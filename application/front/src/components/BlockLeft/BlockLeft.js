import React, { useState, useEffect } from 'react';
import './BlockLeft.css'
import dots from '../../assets/dots.png'
import play_btn from '../../assets/play_btn.svg'
import disabled_play_btn from '../../assets/disabled_play_btn.svg'
import axios from 'axios';


function BlockLeft({setFileName, setStartScrapping}) {
    const [uploadedFileNameLegend, setUploadedFileNameLegend] = useState("Upload Legend");
    const [uploadedFileNameLithologie, setUploadedFileNameLithologie] = useState("Upload Lithologie");
    const [uploadedFileLegend, setUploadedFileLegend] = useState();
    const [uploadedFileLithologie, setUploadedFileLithologie] = useState();
    const [fileList, setFileList] = useState([]);
    //const axios = require("axios")
    function handleChangeLegend(event) {
        setUploadedFileNameLegend(event.target.files[0].name);
        setUploadedFileLegend(event.target.files[0]);
        console.log(uploadedFileNameLegend);
       // setFileName(event.target.files[0].name);
        //setSelectedFile('')
      }

      function handleChangeLithologie(event) {
        setUploadedFileNameLithologie(event.target.files[0].name);
        setUploadedFileLithologie(event.target.files[0]);
        console.log(uploadedFileNameLegend);
       // setFileName(event.target.files[0].name);
        //setSelectedFile('')
      }
    //listReactFiles("../../../../NO_Quad_15").then(files => console.log(files))

    const [selectedFile, setSelectedFile] = useState('');

    function handleFileChange(event) {
      const file = event.target.value;
      setSelectedFile(file);
      setFileName(file); 
    //   setUploadedFileNameLegend("Upload New");
    //   setUploadedFile();
      console.log("file = ", file)
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
        if (uploadedFileNameLegend != 'Upload Legend') {
            var bodyFormData = new FormData();
            bodyFormData.append('uploaded_file', uploadedFileLegend);
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
    }, [uploadedFileNameLegend]);

    useEffect(() => {
        if (uploadedFileNameLithologie!= 'Upload Lithologie') {
            var bodyFormData = new FormData();
            bodyFormData.append('uploaded_file', uploadedFileLithologie);
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
    }, [uploadedFileNameLithologie]);

    return (
        <div className='block-left'> 
            <h1>Completion logs</h1>
            <p>Enter the name of the well on the left and the corresponding legend in the middle and lithologie on the right.</p>
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
                    <span>{uploadedFileNameLegend}</span>
                    <input id='input' className='btn-upload' type="file" name="upload" accept="application/png" placeholder='Upload Legend' onChange={handleChangeLegend}/>
                </label>

                <label className='btn-upload'> 
                    <span>{uploadedFileNameLithologie}</span>
                    <input id='input' className='btn-upload' type="file" name="upload" accept="application/png" placeholder='Upload Lithologie' onChange={handleChangeLithologie}/>
                </label>
            </div>
            <img className='dots' src={dots} alt='dots'/>
            {uploadedFileNameLegend == "Upload Legend" || uploadedFileNameLithologie == "Upload Lithologie"|| selectedFile == ''?  
                <img className='disabled-play-btn' src={disabled_play_btn} alt='disabled play btn'/>:
            <a className='play-btn' href='#results'>
                <img src={play_btn} alt='play btn' onClick={()=>setStartScrapping(true)}/> 
            </a>
            }
        </div>
    );
}

export default BlockLeft;