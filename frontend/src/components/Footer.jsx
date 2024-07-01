import { Button } from 'primereact/button';
import 'primeflex/primeflex.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import '../styles/Footer.css'; 

const Footer = () => {
    return (
        <div className="footer-container">
            <div className="footer-content">
                <h2>Meloturtle</h2>
                <p>I created Meloturtle because I was tired of using Spotify's autogenerated playlists to discover new music. 
                Add or modify the recommendation engines you want and add them here!
                The project is completely open, feel free to use it as you wish!</p>
                <h3>Get in touch!</h3>
                <div className="footer-icons">
                    <Button icon="pi pi-linkedin" className="p-button-rounded p-button-text p-button-plain" onClick={() => window.open('https://www.linkedin.com/in/david-olimpio-silva/', '_blank')} />
                    <Button icon="pi pi-github" className="p-button-rounded p-button-text p-button-plain" onClick={() => window.open('https://github.com/dolimpio', '_blank')} />
                </div>
                <div className="footer-contact">
                    <div className="footer-link">
                        <i className="pi pi-envelope"></i>
                        <a href="mailto:david@email.com">david@email.com</a>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Footer;