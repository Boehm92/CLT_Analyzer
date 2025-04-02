import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function GET() {
    try {
        const templatesDir = path.join(process.cwd(), "public/machiningFeatureTemplates");

        // Überprüfe, ob der Ordner existiert
        if (!fs.existsSync(templatesDir)) {
            console.error("📁 Fehler: Der Ordner machiningFeatureTemplates existiert nicht.");
            return NextResponse.json({ error: "Ordner existiert nicht" }, { status: 404 });
        }

        // Lade alle Bilddateien aus dem Ordner
        const files = fs.readdirSync(templatesDir).filter(file => file.toLowerCase().endsWith(".png"));

        console.log("📸 Gefundene Bilder:", files);

        return NextResponse.json(files);
    } catch (error) {
        console.error("❌ Fehler beim Laden der MachiningFeatureTemplates:", error);
        return NextResponse.json({ error: "Serverfehler" }, { status: 500 });
    }
}
