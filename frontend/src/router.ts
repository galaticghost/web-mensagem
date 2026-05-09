import { createBrowserRouter, redirect  } from "react-router"
import RootLayout from "./layout/RootLayout"
import AuthLayout from "./layout/AuthLayout"
import Register from "./routes/Register"
import Login from "./routes/Login"
import Chat from "./routes/Chat"

export const router = createBrowserRouter([
    {
        path: "/",
        loader: () => redirect("/chat")
    },
    
    {
        path: "/",
        Component: RootLayout,
        
        children: [{
            path: "auth",
            Component: AuthLayout,
            children: [
                { path: "login", Component: Login },
                { path: "register", Component: Register }
            ]
        },
        {
            path: "chat",
            Component: Chat
        }
        ]
    }
])