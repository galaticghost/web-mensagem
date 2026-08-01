export async function createPrivateChat(userId: number) {
    const url = "http://127.0.0.1:8000/api/chats/private";

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `${localStorage.getItem("token_type")} ${localStorage.getItem("access_token")}`
            },
            body: JSON.stringify({
                user_id: userId // id do usuário que se queira criar um chat
            })
        });

        const data = await response.json();

        if (!response.ok) { throw new Error(data.detail || "Error register"); }

        return data;
    } catch (error: unknown) {
        if (error instanceof Error) {
            console.error(error.message);
        }
        throw error;
    }


}