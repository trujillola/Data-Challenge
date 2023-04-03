import React, { useState, useEffect } from 'react';
import './BlockLeft.css'
import dots from '../../assets/dots.png'
import play_btn from '../../assets/play_btn.svg'
import disabled_play_btn from '../../assets/disabled_play_btn.svg'
import axios from 'axios';
import Deep from '../Deep/Deep';


function BlockLeft({setFileName, setStartScrapping, startScrapping}) {
    const [uploadedFileName, setUploadedFileName] = useState("Upload New");
    const [uploadedFile, setUploadedFile] = useState();
    const [fileList, setFileList] = useState([]);
    //const axios = require("axios")
    function handleChange(event) {
        setUploadedFileName(event.target.files[0].name);
        setUploadedFile(event.target.files[0]);
        console.log(uploadedFileName);
        setStartScrapping(false);
        console.log("startscrapping = ", startScrapping)
       // setFileName(event.target.files[0].name);
        //setSelectedFile('')
      }
    //listReactFiles("../../../../NO_Quad_15").then(files => console.log(files))

    const [selectedFile, setSelectedFile] = useState('');

    function handleFileChange(event) {
      const file = event.target.value;
      setSelectedFile(file);
      setFileName(file); 
    //   setUploadedFileName("Upload New");
    //   setUploadedFile();
      console.log("file = ", file)
      setStartScrapping(false);
      console.log("startscrapping = ", startScrapping)
    }
  
   // const fileList = ['fichier1.pdf', 'fichier2.pdf', 'fichier3.pdf'];
   
    useEffect(() => {
        console.log("ici");
            axios.get('http://127.0.0.1:8000/api/get_files_list/')
            .then(function (response) {
                setFileList(response.data)
                console.log("coucou");
                console.log(response);
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
   
    
    useEffect(() => {
        if (uploadedFileName != 'Upload New') {
            var bodyFormData = new FormData();
            bodyFormData.append('uploaded_file', uploadedFile);
            axios({
                method: "post",
                url: "http://127.0.0.1:8000/api/upload_file/",
                data: bodyFormData,
                headers: { "Content-Type": "multipart/form-data" },
              })
                .then(function (response) {
                    //setFileList(response.data)
                    console.log("coucou");
                    console.log(response);
                })
                .catch(function (error) {
                    console.log(error);
                })
                .finally(() => {
                    console.log('finally')
                    //setLoading(false);
                });
        }
    }, [uploadedFileName]);

    return (
        <div className='block-left'> 
            <h1>Completion logs</h1>
            <p>Enter the name of the well on the left and the corresponding lithologie on the right.</p>
            <div className='btn'>
                {/* <button className='btn-select'>Select completion log</button> */}
                <input className='btn-input' placeholder="15_3-2"  value={selectedFile} onChange={handleFileChange}></input>
            
                {/* <select  id="file-select" className='btn-select' value={selectedFile} onChange={handleFileChange}>
                    <option value="">-- Select completion log --</option>
                    {fileList.map((file) => (
                    <option key={file} value={file}>
                        {file}
                    </option>
                    ))}
                </select> */}
 
                <label className='btn-upload'> 
                    <span>{uploadedFileName}</span>
                    <input id='input' className='btn-upload' type="file" name="upload" accept="application/png" placeholder='Upload New' onChange={handleChange}/>
                </label>
            </div>
            <Deep></Deep>
            <img className='dots' src={dots} alt='dots'/>
            {uploadedFileName == "Upload New" || selectedFile == ''?  
                <img className='disabled-play-btn' src={disabled_play_btn} alt='disabled play btn'/>:
            <a className='play-btn' href='#results'>
                <img src={play_btn} alt='play btn' onClick={()=>setStartScrapping(true)}/> 
            </a>
            }
        </div>
    );
}

export default BlockLeft;