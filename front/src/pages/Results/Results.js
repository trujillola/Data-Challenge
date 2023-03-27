import React, { useState, useEffect } from 'react';
import './Results.css';
import { Pie3D } from 'react-pie3d'
import '../../styles/colors.css'
import axios from 'axios'
function Results(props) {
    const[data, setData] = useState([]);
    useEffect(() => {
        console.log("ici");
            axios.get('http://127.0.0.1:8000/api/get_well_composition/', {params : {file_name: '15_2-1__WELL__15-02-01_PB-706-0386.pdf'}})
            .then(function (response) {
                setData(response.data)
                console.log("coucou");
                console.log(response.data);
            })
            .catch(function (error) {
                console.log(error);
            })
            .finally(() => {
                console.log('finally')
                //setLoading(false);
            });
        console.log("laaaa");
    }, []);
    const data2 = [
        { value: 10, label: 'apples', color: '#ffc800' }, 
        { value: 20, label: 'bananas', color: '#28c896' },
        { value: 30, label: 'oranges', color: '#96e600' },
        { value: 20, label: 'oranges', color: '#32c8c8' },
      ]
      console.log(data2)
    return (
        <div className='results' id='main'> 
            <h1>coucou</h1>
            <Pie3D config={{size: 0.6, ir: 0, height: 80, angle: 60, strokeWidth:5}} data={data} />
        </div>
    );
}

export default Results;