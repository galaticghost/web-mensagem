import { API_URL } from "../config";
import { authorizedFetch } from "../utils/utils";

export async function searchUsers(username: string) {
    const url = `${API_URL}/api/users/search?username=${encodeURIComponent(username)}`;
    const response = await authorizedFetch(url);
    return response.json();
}