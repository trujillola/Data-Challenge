import axios from 'axios';
import React, { useEffect, useState } from 'react';
import './WellDescription.css'
import Loading from '../Loading/Loading'

function WellDescription({fileName, startScrapping}) {
    const[wellDescription, setWellDescription] = useState([]);
    const[loading, setLoading] = useState(true)
    useEffect(() => {
        if(startScrapping){
            axios.get('http://127.0.0.1:8000/api/get_well_description/', {params : {file_name: fileName}})
            .then(function (response) {
                setWellDescription(response.data)
            })
            .catch(function (error) {
                console.log(error);
            })
            .finally(() => {
                console.log('finally')
                setLoading(false);
            });
        }
    }, [startScrapping]);
    return (
        <div className='description'>
            {loading? 
             <Loading></Loading> :
            <>
                <h2>Details</h2>
                <span>Depth: {wellDescription.depth}</span>
                <span>Description: {wellDescription.description}</span>
            </>
            }
        </div>
    );
}

export default WellDescription;