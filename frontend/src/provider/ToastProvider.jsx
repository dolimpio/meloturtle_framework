import React, { createContext, useContext, useRef } from "react";
import { Toast } from "primereact/toast";

// create context
const ToastContext = createContext(undefined);

// wrap context provider to add functionality
const ToastProvider = ({ children }) => {
  const toastRef = useRef(null);

  const showToast = (options) => {
    if (!toastRef.current) return;
    toastRef.current.show(options);
  };

  return (
    <ToastContext.Provider value={{ showToast }}>
      <Toast ref={toastRef} />
      <div className="toast-wrapper">{children}</div>
    </ToastContext.Provider>
  );
};

export const useToast = () => {
  const context = useContext(ToastContext);

  if (!context) {
    throw new Error(
      "useToastContext have to be used within ToastContextProvider"
    );
  }

  return context;
};

export default ToastProvider;