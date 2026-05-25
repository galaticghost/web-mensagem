import { createBrowserRouter, redirect } from "react-router"
import RootLayout from "./layout/RootLayout"
import AuthLayout from "./layout/AuthLayout"
import Register from "./routes/Register"
import Login from "./routes/Login"
import Chat from "./routes/Chat"
import ProtectedRoute from "./components/ProtectedRoute"

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
            element: (
                <ProtectedRoute>
                    <Chat />
                </ProtectedRoute>
            ),

            children: [{
                path: "tututi",
                element: (
                    <h1>OIEEEEE</h1>
                )
            }]
        }
        ]
    }
])