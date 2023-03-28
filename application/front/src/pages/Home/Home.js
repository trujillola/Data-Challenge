import React from 'react';
import './Home.css';
import Header from '../../components/Header/Header';
import Main from '../../components/Main/Main';

function Home(props) {
    return (
        <div className='home'>
            <Header></Header>
            <Main></Main>
        </div> 
    );
}

export default Home;