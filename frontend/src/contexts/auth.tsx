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
        const storedUser = localStorage.getItem("user");

        if (token && storedUser) {
            setAccessToken(token);
            setUser(JSON.parse(storedUser));
        }
        setIsLoading(false);
    }, []);

    async function login(credentials: UserLogin) {
        const data = await loginRequest(credentials);

        setAccessToken(data.access);

        setUser(data.user);

        localStorage.setItem("access", data.access);
        //localStorage.setItem("refresh", data.refresh);
        localStorage.setItem("user", JSON.stringify(data.user));
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
        //localStorage.removeItem("refresh");
        localStorage.removeItem("user");
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