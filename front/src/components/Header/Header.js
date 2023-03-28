import React from 'react';
import './Header.css';
import logo_cytech from '../../assets/CY_Tech.png'
import logo_total from '../../assets/total-logo.png'
function Header(props) {
    return (
        <div className='header'>
            <img className='logo-total' src={logo_total} alt='logo-total'/>
            <img className='logo-cytech' src={logo_cytech} alt='logo-cytech'/>
        </div>
    );
}

export default Header;