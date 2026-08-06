import { refresh } from "../service/authService";

export async function authorizedFetch(url: string, init?: RequestInit): Promise<Response> {

    const accessToken = localStorage.getItem("access_token");
    const tokenType = localStorage.getItem("token_type");

    let response = await fetch(url, {
        ...init,
        headers: {
            ...init?.headers,
            "Authorization": accessToken
                ? `${tokenType} ${accessToken}`
                : "",
        }
    });

    if (response.ok) return response;

    const errorData = await response.json();

    if (
        response.status === 401 &&
        errorData.detail === "TOKEN_EXPIRED"
    ) {
        const refreshToken = localStorage.getItem("refresh_token");

        if (!refreshToken) {
            localStorage.clear();
            throw new Error("NO_REFRESH_TOKEN");
        }

        try {
            const tokens = await refresh(refreshToken);

            localStorage.setItem("access_token", tokens.access_token);
            localStorage.setItem("refresh_token", tokens.refresh_token);
            localStorage.setItem("token_type", tokens.token_type);

            response = await fetch(url, {
                ...init,
                headers: {
                    ...init?.headers,
                    "Authorization": `${tokens.token_type} ${tokens.access_token}`,
                },
            });

            if (!response.ok) {
                throw new Error("REQUEST_FAILED_AFTER_REFRESH");
            }

            return response;

        } catch {
            localStorage.clear();
            window.location.href = "/auth/login"; // mudar para router TODO
            throw new Error("SESSION_EXPIRED");

        }
    }

    throw new Error(errorData.detail || "UNKNOWN_ERROR");
}