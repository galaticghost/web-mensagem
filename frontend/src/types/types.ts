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
    refreshToken: string | null;
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

export type WebsocketMessage = {
    type: string;
    content: ReceivedMessage
}

export type Notification = {
    chatId: number;
    count: number;
}

export type ReceivedMessage =
    | {
        type: "new_chat";
        content: Chat
    }
    | {
        type: "message";
        content: Message
    }


export type Message = {
    id: number;
    message: string;
    chat_id: number;
    sender_id: number;
    created_at: string;
}

export type ChatListResponse = {
    chats: Chat[];
};

export type Chat = {
    id: number;
    type: string;
    display_name: string;
    description: string | null;
    created_at: string;
    updated_at: string;
    last_message_id: number | null;
    last_message_at: string
    users_id: number[]
}

