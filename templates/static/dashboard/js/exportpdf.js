document.getElementById("exportarPDF").addEventListener("click", async () => {
  const { jsPDF } = window.jspdf;
  const pdf = new jsPDF({
    orientation: "portrait",
    unit: "px",
    format: "a4",
    compress: true,
  });

  const container = document.getElementById("all-graphs");

  await html2canvas(container, { scale: 2 }).then((canvas) => {
    const imgData = canvas.toDataURL("image/png");

    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();

    const imgProps = pdf.getImageProperties(imgData);
    const imgWidth = pageWidth - 20;
    const imgHeight = (imgProps.height * imgWidth) / imgProps.width;

    pdf.addImage(imgData, "PNG", 10, 10, imgWidth, imgHeight);
    pdf.save("graficos.pdf");
  });
});
