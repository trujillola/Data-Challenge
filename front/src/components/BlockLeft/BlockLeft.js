import React, { useState } from 'react';
import './BlockLeft.css'
import dots from '../../assets/dots.png'
import play_btn from '../../assets/play_btn.svg'


function BlockLeft(props) {
    const [fileName, setFileName] = useState("Upload New");
    function handleChange(event) {
        setFileName(event.target.files[0].name)
      }
    //listReactFiles("../../../../NO_Quad_15").then(files => console.log(files))

    const [selectedFile, setSelectedFile] = useState('');

    function handleFileChange(event) {
      const file = event.target.value;
      setSelectedFile(file);
    }
  
    const fileList = ['fichier1.pdf', 'fichier2.pdf', 'fichier3.pdf'];
   
   
    return (
        <div className='block-left'>
            <h1>Completion logs</h1>
            <p>A thoughtful combination of design and function to support your everyday movement. Limited stocks. Shop now.</p>
            <div className='btn'>
                {/* <button className='btn-select'>Select completion log</button> */}

            
                <select disabled={fileName != 'Upload New'? true : false} id="file-select" className={fileName != 'Upload New'? 'btn-select-disabled':'btn-select'} value={selectedFile} onChange={handleFileChange}>
                    <option value="">-- Select completion log --</option>
                    {fileList.map((file) => (
                    <option key={file} value={file}>
                        {file}
                    </option>
                    ))}
                </select>
 
                <label className={selectedFile != ''? 'btn-upload-disabled':'btn-upload'} > 
                    <span>{fileName}</span>
                    <input disabled={selectedFile != ''? true : false} className='btn-upload' type="file" name="upload" accept="application/pdf" placeholder='Upload New' onChange={handleChange}/>
                </label>
            </div>
            <img className='dots' src={dots} alt='dots'/>
            <img className='play_btn' src={play_btn} alt='play btn'/>
        </div>
    );
}

export default BlockLeft;