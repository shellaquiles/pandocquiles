// ==============================================================================
// Google Apps Script Webhook para PanDocquiles
// Agradecimiento especial a @m1gl0 por la contribución de este módulo.
// Instrucciones de despliegue en el README.md
// ==============================================================================

// TODO: Reemplaza esto con el ID de la carpeta de Drive donde quieres guardar los archivos
const FOLDER_ID = "TU_CARPETA_DE_DRIVE_ID_AQUI";

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const contentType = data.fileDataUrl.match(/data:(.*);base64/)[1];
    const base64Str = data.fileDataUrl.split('base64,')[1];
    const decodedBytes = Utilities.base64Decode(base64Str);
    const blob = Utilities.newBlob(decodedBytes, contentType, data.filename);
    
    let isDoc = data.filename.endsWith('.html') || data.filename.endsWith('.docx');
    let targetTitle = isDoc ? data.filename.replace(/\.(html|docx)$/, '') : data.filename;
    let fileUrl;

    // 1. Buscar si ya existe un archivo con ese nombre exacto
    const folder = DriveApp.getFolderById(FOLDER_ID);
    const existingFiles = folder.getFilesByName(targetTitle);
    
    let existingFileId = null;
    
    // 2. Tomamos el primero y borramos los demás para limpiar tu Drive
    if (existingFiles.hasNext()) {
      existingFileId = existingFiles.next().getId();
      // Mandar a la papelera los clones
      while (existingFiles.hasNext()) {
        existingFiles.next().setTrashed(true);
      }
    }

    // 3. Crear o Actualizar
    if (isDoc) {
      if (existingFileId) {
        // ACTUALIZAR Doc Existente (Mantiene su URL)
        const updated = Drive.Files.update({title: targetTitle}, existingFileId, blob, {convert: true});
        fileUrl = updated.alternateLink;
      } else {
        // CREAR Nuevo Doc
        const resource = {
          title: targetTitle,
          mimeType: 'application/vnd.google-apps.document',
          parents: [{id: FOLDER_ID}]
        };
        const newFile = Drive.Files.insert(resource, blob, {convert: true});
        fileUrl = newFile.alternateLink;
      }
    } else { // Es PDF
      if (existingFileId) {
        // ACTUALIZAR PDF Existente (Mantiene su URL)
        const updated = Drive.Files.update({title: targetTitle}, existingFileId, blob);
        fileUrl = updated.alternateLink;
      } else {
        // CREAR Nuevo PDF
        const resource = {
          title: targetTitle,
          parents: [{id: FOLDER_ID}]
        };
        const newFile = Drive.Files.insert(resource, blob);
        fileUrl = newFile.alternateLink;
      }
    }

    return ContentService.createTextOutput(JSON.stringify({
      status: 'success', 
      url: fileUrl
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      status: 'error', 
      message: error.toString(),
      stack: error.stack
    })).setMimeType(ContentService.MimeType.JSON);
  }
}
