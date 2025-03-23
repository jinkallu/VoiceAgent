import React, { useState } from "react";

const FileUpload = ({token}) => {
    const [pdfFile, setPdfFile] = useState(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];

        if (file && file.type === "application/pdf") {
            setPdfFile(file);
        } else {
            alert("Please upload a valid PDF file.");
        }
    };

    const handleUpload = () => {
        if (!pdfFile) return;

        // Example: handle the upload logic (e.g., send to server)
        const formData = new FormData();
        formData.append("file", pdfFile);

        // For now, just logging the file name
        console.log("Uploading:", pdfFile.name);

        // Uncomment and adjust if using a real API:
        fetch("http://127.0.0.1:8000/upload/", {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
            },
            body: formData,
        }).then(response => console.log("Uploaded")).catch(err => console.error(err));
    };

    return (
        <div className="p-4">
            <input type="file" accept="application/pdf" onChange={handleFileChange} />
            {pdfFile && <p>Selected file: {pdfFile.name}</p>}
            <button onClick={handleUpload} className="mt-2 bg-blue-500 text-white px-4 py-2 rounded">
                Upload PDF
            </button>
        </div>
    );
}

export default FileUpload;