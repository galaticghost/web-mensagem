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
    username: string;
    id: number;
}

export type AuthContextType = {
    user: User | null;
    accessToken: string | null;
    tokenType: string | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    register: (formData: UserRegister) => Promise<void>;
    login: (credentials: UserLogin) => Promise<void>;
    logout: () => void;
}

export type SendMessage = {
    message: string;
    chatId: number;
}

export type RecivedMessage = {
    id: number;
    message: string;
    chat_id: number;
    sender_id: number;
    created_at: string;
}

