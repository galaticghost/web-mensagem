export async function searchUsers(username: string) {
    const url = `http://127.0.0.1:8000/api/users/search?username=${encodeURIComponent(username)}`;
    try {
        const response = await fetch(url);
        const data = await response.json();
        console.log(data);
        if (!response.ok) { throw new Error(data.detail || "Error Register") }
        return data;
    } catch (error: unknown) {
        if (error instanceof Error) {
            console.error(error.message);
        }
        throw error
    }
}