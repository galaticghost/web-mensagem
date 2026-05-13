export type UserRegister = {
    username: string;
    email: string;
    password: string;
    password2: string;
}

export type UserLogin = {
    email: string;
    password: string;
}

export type User = {
    email: string;
}

export type AuthContextType = {
    user: User | null;
    accessToken: string | null;
    isAuthenticated: boolean;
}