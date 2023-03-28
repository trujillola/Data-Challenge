import axios from 'axios';
import React, { useEffect, useState } from 'react';

function WellDescription(props) {
    const[wellDescription, setWellDescription] = useState([]);
    useEffect(() => {
            axios.get('http://127.0.0.1:8000/api/get_well_description/', {params : {file_name: '15_2-1__WELL__15-02-01_PB-706-0386.pdf'}})
            .then(function (response) {
                setWellDescription(response.data)
            })
            .catch(function (error) {
                console.log(error);
            })
            .finally(() => {
                console.log('finally')
                //setLoading(false);
            });
    }, []);
    return (
        <div>
            {wellDescription}
        </div>
    );
}

export default WellDescription;