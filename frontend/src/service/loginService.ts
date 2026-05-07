export async function registerUser(data) {
    const url = "http://127.0.0.1:8000/api/";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "applications/json"
            },
            body: JSON.stringify(data)
        })
        if (!response.ok) {throw new Error("Azideia")}

        return await response.json();

    } catch (error: unknown) {
        if (error instanceof Error ) {
            console.error(error.message);
        }
    }
}