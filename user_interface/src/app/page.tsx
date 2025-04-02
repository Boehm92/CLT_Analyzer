"use client";

import React, { useState } from "react";
import { Container, Dialog, DialogActions, DialogContent, DialogTitle, Input, Box } from "@mui/material";
import WireframeViewer from "@/components/WireframeViewer/WireframeViewer";
import InfoBox from "@/components/InfoBox/InfoBox";
import STLFileList from "@/components/STLFileList/STLFileList";
import TitleBar from "@/components/TitleBar/TitleBar";
import MachiningFeatureDisplay from "@/components/MachiningFeatureDisplay/MachiningFeatureDisplay";
import { handleFileUpload, handleSelectFile, STLFile } from "@/utils/fileService";

export default function Home() {
    const [fileUrl, setFileUrl] = useState<string | null>(null);
    const [open, setOpen] = useState(false);
    const [files, setFiles] = useState<STLFile[]>([]);
    const [features, setFeatures] = useState<number[][]>([]);
    const [predictedLabels, setPredictedLabels] = useState<number[]>([]);
    const [mfrFeatures, setMfrFeatures] = useState<number[]>([]);
    const [combinedResponse, setCombinedResponse] = useState<{ volume: number, body_center: number[], length: number, width: number, height: number, time: number } | null>(null);

    const handleFileUploadWrapper = async (event: React.ChangeEvent<HTMLInputElement>) => {
        await handleFileUpload(event, setFiles, setFileUrl, setOpen);
    };

    const handleSelectFileWrapper = async (fileUrl: string) => {
        await handleSelectFile(fileUrl, setFileUrl, setFeatures, setPredictedLabels, setMfrFeatures, setCombinedResponse);
    };

    const handleDeleteFile = (fileName: string) => {
        setFiles((prev) => prev.filter((file) => file.name !== fileName));
    };

    return (
        <>
            <TitleBar onUploadClick={() => setOpen(true)} />
            <Container sx={{ minHeight: "100vh", minWidth: "100vw", backgroundColor: "#3c3c3c", paddingTop: "100px" }}>
                <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", width: "100%" }}>
                    <Box sx={{ display: "flex", justifyContent: "center", gap: 4, width: "100%", maxWidth: "1200px" }}>
                        <STLFileList files={files} onSelectFile={handleSelectFileWrapper} onDeleteFile={handleDeleteFile} />
                        <WireframeViewer
                            fileUrl={fileUrl || ""}
                            features={features || []}
                            predictedLabels={predictedLabels || []}
                        />
                        <InfoBox combinedResponse={combinedResponse} />
                    </Box>
                    <Box sx={{ display: "flex", justifyContent: "center", marginTop: 0, width: "100%", maxWidth: "1200px" }}>
                        <MachiningFeatureDisplay selectedFeatures={mfrFeatures.map(feature => Boolean(feature))} />
                    </Box>
                </Box>

                {/* Upload Dialog */}
                <Dialog open={open} onClose={() => setOpen(false)}>
                    <DialogTitle>Upload STL File</DialogTitle>
                    <DialogContent>
                        <Input type="file" onChange={handleFileUploadWrapper} inputProps={{ accept: ".stl" }} />
                    </DialogContent>
                    <DialogActions>
                        <button onClick={() => setOpen(false)}>Cancel</button>
                    </DialogActions>
                </Dialog>
            </Container>
        </>
    );
}
