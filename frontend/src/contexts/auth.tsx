import { createContext, useEffect, useState, type ReactNode } from "react"
import { login as loginRequest, register as registerRequest } from "../service/authService"
import type { User, AuthContextType, UserLogin, UserRegister } from "../types/types";

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [accessToken, setAccessToken] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    const isAuthenticated = !!accessToken;

    useEffect(() => {
        const token = localStorage.getItem("access");
        const email = localStorage.getItem("email");

        if (token && email) {
            setAccessToken(token);
            setUser({ email });
        }
        setIsLoading(false);
    }, []);

    async function login(credentials: UserLogin) {
        const data = await loginRequest(credentials);

        setAccessToken(data.access);

        setUser({
            email: credentials.email
        });

        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        localStorage.setItem("email", credentials.email);
    }

    async function register(formData: UserRegister) {
        await registerRequest(formData);

        await login({
            email: formData.email,
            password: formData.password
        })
    }

    function logout() {
        setUser(null);
        setAccessToken(null);
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        localStorage.removeItem("email");
    }

    return (
        <AuthContext.Provider
            value={{
                user,
                accessToken,
                isAuthenticated,
                isLoading,
                register,
                login,
                logout
            }}>
            {children}
        </AuthContext.Provider>
    )
}

export const AuthContext = createContext<AuthContextType | null>(null);