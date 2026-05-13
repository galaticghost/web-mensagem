import type { UserRegister, UserLogin } from "../types/types";

export async function register(formData: UserRegister) {
    const url = "http://127.0.0.1:8000/api/register/";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        })
        
        const data = await response.json();
        
        if (!response.ok) { throw new Error(data.detail || "Erro ao registrar") }

        return data;
    } catch (error: unknown) {
        if (error instanceof Error) {
            console.error(error.message);
        }
        throw error
    }
}

export async function login(credentials: UserLogin) {
    const url = "http://127.0.0.1:8000/api/login/";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(credentials)
        });
        
        const data = await response.json();
        if (!response.ok) { throw new Error(data.detail || "Erro ao fazer login")}

        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        return data;

    } catch (error: unknown) {
        if (error instanceof Error) {
            console.error(error.message);
        }
        throw error;
    }
}

export function logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("email");
}