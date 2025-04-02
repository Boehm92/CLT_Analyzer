"use client";

import { Box, Typography } from "@mui/material";

export default function InfoBox({ combinedResponse }: { combinedResponse: { volume: number, body_center: number[], length: number, width: number, height: number, time: number } | null }) {
    return (
        <Box
            sx={{
                width: "20vw",
                minWidth: "200px",
                height: "40vw",
                maxHeight: "400px",
                borderRadius: 2,
                bgcolor: "#787474",
                boxShadow: "3px 3px 10px rgba(0,0,0,0.2)",
                padding: 2,
                overflowY: "auto",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                color: "white",
            }}
        >
            <Typography variant="h6" sx={{ fontWeight: "bold", marginBottom: 1 }}>
                ● Dimensions:
            </Typography>
            <Typography sx={{ marginLeft: 2 }}>
                • <b>Length:</b> {combinedResponse?.length?.toFixed(2) || "0.00"} mm <br />
                • <b>Width:</b> {combinedResponse?.width?.toFixed(2) || "0.00"} mm <br />
                • <b>Height:</b> {combinedResponse?.height?.toFixed(2) || "0.00"} mm <br />
                • <b>Volume:</b> {combinedResponse?.volume?.toFixed(2) || "0.00"} mm³
            </Typography>

            <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>
                ● Center of Gravity:
            </Typography>
            <Typography sx={{ marginLeft: 2 }}>
                • <b>X:</b> {combinedResponse?.body_center[0]?.toFixed(2) || "0.00"} mm <br />
                • <b>Y:</b> {combinedResponse?.body_center[1]?.toFixed(2) || "0.00"} mm <br />
                • <b>Z:</b> {combinedResponse?.body_center[2]?.toFixed(2) || "0.00"} mm
            </Typography>

            <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>
                ● Production:
            </Typography>
            <Typography sx={{ marginLeft: 2 }}>
                • <b>Post-processing:</b> {combinedResponse?.time?.toFixed(2) || "0.00"} min
            </Typography>
        </Box>
    );
}
