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
    isLoading: boolean;
    register: (formData: UserRegister) => Promise<void>;
    login: (credentials: UserLogin) => Promise<void>;
    logout: () => void;
}