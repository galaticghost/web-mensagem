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