import React from 'react';
import './Home.css';
import Header from '../../components/Header/Header';
import Main from '../../components/Main/Main';

function Home({setFileName}) {
    return (
        <div className='home' id='home'>
            <Header></Header>
            <Main setFileName={setFileName}></Main>
        </div> 
    );
}

export default Home;