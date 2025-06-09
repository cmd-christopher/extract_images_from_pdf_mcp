import fitz  # PyMuPDF
import io # Keep for BytesIO if needed elsewhere, though maybe not for this specific change
import os
import argparse
# from PIL import Image # No longer directly used for saving

def extract_images(pdf_path, output_dir):
    """
    Extracts images from a PDF file and saves them as PNG files in the specified output directory.

    Args:
        pdf_path (str): The path to the input PDF file.
        output_dir (str): The path to the directory where extracted images will be saved.
    """
    try:
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")

        # Open the PDF file
        doc = fitz.open(pdf_path)
        print(f"Opened PDF: {pdf_path}")

        image_count = 0
        extracted_images = 0

        # Iterate through each page
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images(full=True)
            
            if image_list:
                print(f"Found {len(image_list)} image(s) on page {page_num + 1}")
            
            for img_index, img_info in enumerate(image_list):
                image_count += 1
                # xref = img_info[0] # XREF of the image, not directly used in this new approach
                
                # Render the image region from the page to capture its appearance
                try:
                    # Get the bounding box of the image on the page
                    # Pass the full img_info item from page.get_images(full=True)
                    bbox = page.get_image_bbox(img_info) 
                    
                    # Render the specific area of the page defined by the bbox
                    # alpha=False ensures it's rendered on the page background (typically white)
                    pix = page.get_pixmap(clip=bbox, alpha=False) 
                    
                    # Construct image filename
                    image_filename = f"image_p{page_num + 1}_{img_index + 1}.png"
                    output_path = os.path.join(output_dir, image_filename)
                    
                    # Save the rendered Pixmap as PNG
                    pix.save(output_path)
                    print(f"Saved: {output_path}")
                    extracted_images += 1
                except Exception as e:
                    print(f"Error processing image {image_count} (item: {img_info[0]}) on page {page_num + 1} using page rendering: {e}")
                finally:
                    pix = None # Release Pixmap resources

        if extracted_images == 0:
            print(f"No images were extracted from {pdf_path}.")
        else:
            print(f"Successfully extracted {extracted_images} image(s) to {output_dir}")

    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
    except fitz.FitzError as e: # More specific PyMuPDF error
        print(f"Error opening or processing PDF file {pdf_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if 'doc' in locals() and doc:
            doc.close()
            print(f"Closed PDF: {pdf_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract images from a PDF file and save them as PNGs.")
    parser.add_argument("pdf_path", help="Path to the input PDF file.")
    parser.add_argument("output_dir", help="Path to the directory to save extracted PNG images.")

    args = parser.parse_args()

    print(f"Starting image extraction...")
    print(f"Input PDF: {args.pdf_path}")
    print(f"Output Directory: {args.output_dir}")
    
    extract_images(args.pdf_path, args.output_dir)
