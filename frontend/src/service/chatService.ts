import { API_URL } from "../config";
import { authorizedFetch } from "../utils/utils";

export async function createPrivateChat(userId: number) {
    const url = `${API_URL}/api/chats/private`;

    const response = await authorizedFetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            user_id: userId // id do usuário que se queira criar um chat
        })
    });

    return response.json();
}

export async function getUserChats() {
    const url = `${API_URL}/api/chats/userchats`;
    const response = await authorizedFetch(url);

    return response.json();
}

export async function getMessageHistory(chatId: number) {
    const url = `${API_URL}/api/chats/${chatId}/messages`;

    const response = await authorizedFetch(url);

    return response.json();
}