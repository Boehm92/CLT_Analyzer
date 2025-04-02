import { Box, Typography, List, ListItem, ListItemButton, ListItemText, IconButton } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";

interface STLFile {
    name: string;
    url: string;
    file: File;
}

interface STLFileListProps {
    onSelectFile: (fileUrl: string) => void;
    files: STLFile[];
    onDeleteFile: (fileName: string) => void;
}

export default function STLFileList({ onSelectFile, files, onDeleteFile }: STLFileListProps) {
    return (
        <Box
            sx={{
                width: "20vw",
                minWidth: "200px",
                height: "40vw",
                maxHeight: "400px",
                backgroundColor: "#787474",
                padding: 2,
                borderRadius: 2,
                boxShadow: "3px 3px 10px rgba(0,0,0,0.2)",
                overflowY: "auto",
                "&::-webkit-scrollbar": {
                    width: "8px",
                },
                "&::-webkit-scrollbar-track": {
                    backgroundColor: "#555",
                    borderRadius: "10px",
                },
                "&::-webkit-scrollbar-thumb": {
                    backgroundColor: "#333",
                    borderRadius: "10px",
                },
                "&::-webkit-scrollbar-thumb:hover": {
                    backgroundColor: "#555",
                },
            }}
        >
            <Typography align={"center"} variant="h6" sx={{ fontWeight: "bold", marginTop: 2, color: "#ffffff" }}>
                STL-Dateien
            </Typography>
            {files.length === 0 ? (
                <Typography textAlign="center" sx={{ color: "#ffffff" }}>
                    Keine Dateien
                </Typography>
            ) : (
                <List>
                    {files.map((file) => (
                        <ListItem key={file.name} disablePadding>
                            <ListItemButton onClick={() => onSelectFile(file.url)}>
                                <ListItemText primary={file.name} sx={{ color: "#ffffff" }} />
                            </ListItemButton>
                            <IconButton edge="end" aria-label="delete" onClick={() => onDeleteFile(file.name)}>
                                <DeleteIcon style={{ color: "red" }} />
                            </IconButton>
                        </ListItem>
                    ))}
                </List>
            )}
        </Box>
    );
}
