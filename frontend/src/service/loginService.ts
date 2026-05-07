import type { UserRegister, UserLogin } from "../types/types";

export async function registerUser(data: any) {
    const url = "http://127.0.0.1:8000/api/register/";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        if (!response.ok) { throw new Error("Azideia") } //TODO

        return await response.json();

    } catch (error: unknown) {
        if (error instanceof Error) {
            console.error(error.message);
        }
    }
}

export async function loginUser(credentials: any) {
    const url = "http://127.0.0.1:8000/api/login/";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(credentials)
        });
        if (!response.ok) { throw new Error("Azideia") } //TODO
        const data = await response.json();

        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);

        return data;

    } catch (error: unknown) {
        if (error instanceof Error) {
            console.error(error.message);
        }
    }
}