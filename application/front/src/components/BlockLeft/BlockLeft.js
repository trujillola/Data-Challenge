import React, { useState, useEffect } from 'react';
import './BlockLeft.css'
import dots from '../../assets/dots.png'
import play_btn from '../../assets/play_btn.svg'
import axios from 'axios';


function BlockLeft(props) {
    const [fileName, setFileName] = useState("Upload New");
    const [uploadedFile, setUploadedFile] = useState();
    const [fileList, setFileList] = useState([]);
    //const axios = require("axios")
    function handleChange(event) {
        setFileName(event.target.files[0].name)
        setUploadedFile(event.target.files[0])
        console.log(fileName)
      }
    //listReactFiles("../../../../NO_Quad_15").then(files => console.log(files))

    const [selectedFile, setSelectedFile] = useState('');

    function handleFileChange(event) {
      const file = event.target.value;
      setSelectedFile(file);
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
        if (fileName != 'Upload New') {
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
    }, [fileName]);

    return (
        <div className='block-left'>
            <h1>Completion logs</h1>
            <p>A thoughtful combination of design and function to support your everyday movement. Limited stocks. Shop now.</p>
            <div className='btn'>
                {/* <button className='btn-select'>Select completion log</button> */}

            
                <select disabled={fileName !== 'Upload New'? true : false} id="file-select" className={fileName !== 'Upload New'? 'btn-select-disabled':'btn-select'} value={selectedFile} onChange={handleFileChange}>
                    <option value="">-- Select completion log --</option>
                    {fileList.map((file) => (
                    <option key={file} value={file}>
                        {file}
                    </option>
                    ))}
                </select>
 
                <label className={selectedFile !== ''? 'btn-upload-disabled':'btn-upload'} > 
                    <span>{fileName}</span>
                    <input disabled={selectedFile !== ''? true : false} className='btn-upload' type="file" name="upload" accept="application/pdf" placeholder='Upload New' onChange={handleChange}/>
                </label>
            </div>
            <img className='dots' src={dots} alt='dots'/>
            <a className='play_btn' href='#main'><img src={play_btn} alt='play btn'/></a>
        </div>
    );
}

export default BlockLeft;