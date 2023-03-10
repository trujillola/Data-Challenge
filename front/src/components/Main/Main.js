import React from 'react';
import BlockLeft from '../BlockLeft/BlockLeft';
import './Main.css'
import img_total from "../../assets/mix_homepage.webp"

function Main(props) {
    return (
        <div className='main'>
            <BlockLeft></BlockLeft>
            <img src={img_total} alt="img_total"/>
        </div>
    );
}

export default Main;