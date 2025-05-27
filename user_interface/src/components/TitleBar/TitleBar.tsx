import {AppBar, Toolbar, Typography, Button, Box} from "@mui/material";
import Image from "next/image";

export default function TitleBar({onUploadClick}: { onUploadClick: () => void }) {
    return (
        <AppBar position="fixed" sx={{backgroundColor: "#ff7820", padding: "10px 20px"}}>
            <Toolbar sx={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>
                <Box sx={{marginRight: "auto"}}>
                    <Image
                        src="/Logo_TH.svg"  // Der Pfad sollte absolut oder relativ zum Public-Ordner sein
                        alt="University Logo"
                        width={200}           // Breite des Bildes
                        height={70}          // Höhe des Bildes
                        style={{ objectFit: "contain" }}
                    />
                </Box>

                {/* Titel (Mitte) */}
                <Typography
                    variant="h6"
                    sx={{
                        textAlign: "center",
                        flexGrow: 1,
                        fontSize: "40px",  // Größe wie im Bild
                        fontWeight: "bold",  // Fett wie im Bild
                        color: "white",  // Helle Schrift für guten Kontrast
                    }}
                >
                    CLT-Analyzer
                </Typography>

                <Button
                    variant="outlined"
                    onClick={onUploadClick}
                    sx={{
                        marginRight: "auto",
                        color: "black",
                        borderColor: "black",
                        borderRadius: "50px",
                        padding: "8px 20px",
                        fontSize: "16px",
                        textTransform: "none",
                        backgroundColor: "white",
                        transition: "all 0.3s ease",
                        "&:hover": {
                            color: "#ff7900",
                            borderColor: "#ff7900",
                            backgroundColor: "white",  // Wichtig: Weiß lassen, damit der Button sichtbar bleibt
                        },
                    }}
                >
                    Upload STL File
                </Button>
            </Toolbar>
        </AppBar>
    );
}
