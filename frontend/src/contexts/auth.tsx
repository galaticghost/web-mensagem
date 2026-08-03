import { createContext, useEffect, useState, type ReactNode } from "react";
import { login as loginRequest, register as registerRequest } from "../service/authService";
import { websocket } from "../websockets/socket";
import type { User, AuthContextType, UserLogin, UserRegister } from "../types/types";

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [accessToken, setAccessToken] = useState<string | null>(null);
    const [tokenType, setTokenType] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    const isAuthenticated = !!accessToken;

    useEffect(() => {
        const token = localStorage.getItem("access_token");
        const storedUser = localStorage.getItem("user");
        const storedTokenType = localStorage.getItem("token_type");

        if (token && storedUser) {
            setAccessToken(token);
            setTokenType(storedTokenType);
            setUser(JSON.parse(storedUser));
        }
        setIsLoading(false);
    }, []);

    async function login(credentials: UserLogin) {
        const data = await loginRequest(credentials);

        setAccessToken(data.access_token);

        setUser(data.user);

        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("token_type", data.token_type);
        //localStorage.setItem("refresh", data.refresh);
        localStorage.setItem("user", JSON.stringify(data.user));

        await websocket.connect(data.access_token);
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
        setTokenType(null);
        localStorage.removeItem("access_token");
        localStorage.removeItem("token_type");
        //localStorage.removeItem("refresh");
        localStorage.removeItem("user");

        websocket.disconnect();
    }

    return (
        <AuthContext.Provider
            value={{
                user,
                accessToken,
                tokenType,
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