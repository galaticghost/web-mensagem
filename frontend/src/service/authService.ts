import type { UserRegister, UserLogin } from "../types/types";

export async function register(formData: UserRegister) {
    const url = "http://127.0.0.1:8000/api/auth/register";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        })

        const data = await response.json();

        if (!response.ok) { throw new Error(data.detail || "Error Register") }

        return data;
    } catch (error: unknown) {
        if (error instanceof Error) {
            console.error(error.message);
        }
        throw error;
    }
}

export async function login(credentials: UserLogin) {
    const url = "http://127.0.0.1:8000/api/auth/login";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(credentials)
        });

        const data = await response.json();
        if (!response.ok) { throw new Error(data.detail || "Erro ao fazer login") }

        return data;

    } catch (error: unknown) {
        if (error instanceof Error) {
            console.error(error.message);
        }
        throw error;
    }
}

export async function refresh(refreshToken: string) {
    const url = "http://127.0.0.1:8000/api/auth/refresh";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                refresh_token: refreshToken
            })
        });

        const data = await response.json();
        if (!response.ok) { throw new Error(data.detail || "Erro no refresh") }

        return data;

    } catch (error: unknown) {
        if (error instanceof Error) {
            console.error(error.message);
        }
        throw error;
    }
}