import { createContext, useEffect, useState, type ReactNode } from "react"
import { login } from "../service/authService"
import type { User, AuthContextType } from "../types/types";

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({children} : {children: ReactNode}) {
    const [user, setUser] = useState<User | null>(null);
    const [accessToken, setAccessToken] = useState<string | null>(null);

    const isAuthenticated = !!accessToken;

    useEffect(() => {
        const token = localStorage.getItem("access");
        const email = localStorage.getItem("email");
        
        if (token && email) {
            setAccessToken(token);
            setUser({ email });
        }
    },[]);

    return (
        <AuthContext.Provider
        value={{
            user,
            accessToken,
            isAuthenticated
        }}>
            {children}
        </AuthContext.Provider>
    )
}
