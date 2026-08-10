import { API_URL } from "../config";
import type { User } from "../types/types";
import { authorizedFetch } from "../utils/utils";

export async function searchUsers(username: string): Promise<User[]> {
    const url = `${API_URL}/api/users/search?username=${encodeURIComponent(username)}`;
    const response = await authorizedFetch(url);
    return response.json();
}