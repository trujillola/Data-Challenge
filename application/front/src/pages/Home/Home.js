import React from 'react';
import './Home.css';
import Header from '../../components/Header/Header';
import Main from '../../components/Main/Main';
import Footer from '../../components/Footer/Footer';

function Home({setFileName, setStartScrapping, startScrapping}) {
    return (
        <div className='home' id='home'>
            <Header></Header>
            <Main setFileName={setFileName} setStartScrapping={setStartScrapping} startScrapping={startScrapping}></Main>
            <Footer></Footer>
        </div> 
    );
}

export default Home;