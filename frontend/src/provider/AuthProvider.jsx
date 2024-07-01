import axios from "axios";
import { createContext, useContext, useEffect, useMemo, useState } from "react";

const AuthContext = createContext();

export const meloturtle_api = axios.create({
  baseURL: 'http://localhost:8000/api'
});

const AuthProvider = ({ children }) => {
  // State to hold the authentication token
  const [token, setToken_] = useState(localStorage.getItem("token"));
  const [isTokenSet, setIsTokenSet_] = useState(false);

  // Function to set the authentication token
  const setToken = (newToken) => {
    setToken_(newToken);
  };

  useEffect(() => {
    if (token) {
      meloturtle_api.defaults.headers.common["Authorization"] = token;
      localStorage.setItem('token',token);
      setIsTokenSet_(true);
    } else {
      delete meloturtle_api.defaults.headers.common["Authorization"];
      localStorage.removeItem('token')
      setIsTokenSet_(false);

    }
  }, [token]);

  // Memoized value of the authentication context
  const contextValue = useMemo(
    () => ({
      token,
      setToken,
      isTokenSet,
    }),
    [token, isTokenSet]
  );

  // Provide the authentication context to the children components
  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};

export default AuthProvider;