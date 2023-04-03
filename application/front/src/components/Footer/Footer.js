import React from 'react';
import './Footer.css'

import { library } from '@fortawesome/fontawesome-svg-core';
import { faEnvelope } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

library.add(faEnvelope);


function Footer(props) {
    return (
        // <div className='footer'>
        //     <span>In case of error or questions</span>
        //     <span>Contact us : </span>
        //     <span>close-your-ai@gmail.com</span>
        // </div>
        <div>
        <footer className='footer'>
        <p>In case of errors or questions, contact us !</p>
                <p className='mail'><FontAwesomeIcon icon="envelope"/><a href="mailto:close-your-ai_GP@cy-tech.fr" onClick={() => window.location = 'mailto:close-your-ai_GP@cy-tech.fr'}>close-your-ai_GP@cy-tech.fr</a></p>
                <p>&copy; 2023 Close Your AI</p>
            </footer>
        </div>
       
    );
}

export default Footer;