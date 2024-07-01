import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { useAuth } from "../provider/AuthProvider";
import { ProtectedRoute } from "./ProtectedRoute";

import Layout from "../pages/Layout";
import Home from "../pages/Home";
import Generator from "../pages/Generator";
import SavedPlaylists from '../pages/SavedPlaylists';
import GeneratedPlaylist from '../pages/GeneratedPlaylist';
import Login from '../pages/Login';
import RedirectHandler from '../pages/RedirectHandler';

import About from "../pages/About";
import NoPage from "../pages/NoPage";
import ErrorPage from "../pages/ErrorPage";



const Routes = () => {
    const { token } = useAuth();

    const routesForPublic = [
        {
            path: "/",
            element: <Layout />,
            errorElement: <ErrorPage />,
            children: [
                {
                    path: "/",
                    element: <Home />,
                },
                {
                    path: "/login",
                    element: <Login />, 
                },
                {
                    path: "/about",
                    element: <About />,
                },
                {
                    path: "/redirect",
                    element: <RedirectHandler />, 
                },
                {
                    path: "*",
                    element: <NoPage />, 
                },
            ],
        },

    ];

    const routesForAuthenticatedOnly = [
        {
            path: "/",
            element: <Layout />,
            errorElement: <ErrorPage />,
            children: [
                {
                    path: "/",
                    element: <ProtectedRoute />,
                    children: [
                        {
                            path: "/generator",
                            element: <Generator />,
                        },
                        {
                            path: "/generated-playlist",
                            element: <GeneratedPlaylist />,
                        },
                        {
                            path: "/library",
                            element: <SavedPlaylists />,
                        }, 
                    ],
                },
            ],
        },
    ];

    const routesForNotAuthenticatedOnly = [
        {
            path: "/",
            element: <Layout />,
            errorElement: <ErrorPage />,
            children: [
                {
                    path: "/",
                    element: <Home />,
                },
                {
                    path: "/login",
                    element: <Login />,
                },
            ],
        },
    ];

    const router = createBrowserRouter([
        ...routesForPublic,
        ...(!token ? routesForNotAuthenticatedOnly : []),
        ...routesForAuthenticatedOnly,
    ]);

    return <RouterProvider router={router} />;

};
export default Routes;
