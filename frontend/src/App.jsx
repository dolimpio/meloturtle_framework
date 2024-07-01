import Routes from "./routes";
import { PrimeReactProvider } from 'primereact/api';
import { CookiesProvider } from 'react-cookie';
import { Provider } from 'react-redux'

import store from './store/store'
import AuthProvider from './provider/AuthProvider.jsx';
import ToastProvider from './provider/ToastProvider.jsx';

import 'primereact/resources/themes/vela-green/theme.css';
import 'primereact/resources/primereact.min.css'; //core css
import 'primeicons/primeicons.css'; //icons
import 'primeflex/primeflex.css'; // flex
import './styles/App.css'; // Import your CSS file for styling


function App() {

  return (
    <CookiesProvider defaultSetOptions={{ path: '/' }}>
      <PrimeReactProvider>
      <Provider store={store}>
        <ToastProvider>
          <AuthProvider>
              <Routes />
          </AuthProvider>
        </ToastProvider>
        </Provider>
      </PrimeReactProvider>
    </CookiesProvider>
  )
}

export default App;

