import tkinter as tk
from tkinter import filedialog, messagebox, Canvas
from PIL import Image, ImageTk
import os
from pathlib import Path
from io import BytesIO

class ModernButton(Canvas):
    """Custom button widget using Canvas for full color control"""
    def __init__(self, parent, text, command, bg_color, fg_color='white', 
                 font_size=10, bold=True, hover_color='#4f46e5', width=None, height=45):
        
        # Separate canvas kwargs from custom kwargs
        canvas_kwargs = {
            'height': height,
            'bg': bg_color,
            'highlightthickness': 0
        }
        if width:
            canvas_kwargs['width'] = width
            
        super().__init__(parent, **canvas_kwargs)
        
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.text = text
        self.font_size = font_size
        self.is_hovered = False
        
        font_weight = 'bold' if bold else 'normal'
        self.font = ('Segoe UI', font_size, font_weight)
        self.button_height = height
        
        # Draw button
        self.configure(bg=bg_color)
        self.text_id = self.create_text(
            0, 0,
            text=text, fill=fg_color, font=self.font, anchor='center'
        )
        
        # Position text after widget is created
        self.update_idletasks()
        self.coords(self.text_id, self.winfo_reqwidth() / 2 if width else 50, height / 2)
        
        # Bind events
        self.bind('<Button-1>', lambda e: self.command())
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Configure>', self.on_configure)
        
    def on_configure(self, event):
        # Recenter text when widget resizes
        self.coords(self.text_id, event.width / 2, event.height / 2)
        
    def on_enter(self, event):
        self.is_hovered = True
        self.configure(bg=self.hover_color)
        self.configure(cursor='hand2')
        
    def on_leave(self, event):
        self.is_hovered = False
        self.configure(bg=self.bg_color)
        
    def set_bg(self, color):
        self.bg_color = color
        if not self.is_hovered:
            self.configure(bg=color)

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resizer Pro by SamSeen")
        self.root.geometry("1400x900")

        # Bring window to front and focus
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        self.root.focus_force()

        # Modern color scheme
        self.colors = {
            'bg': '#1a1a1a',
            'sidebar': '#252525',
            'card': '#2d2d2d',
            'hover': '#3a3a3a',
            'primary': '#6366f1',
            'primary_hover': '#4f46e5',
            'success': '#10b981',
            'text': '#e5e5e5',
            'text_dim': '#9ca3af',
            'border': '#3f3f3f',
            'accent': '#8b5cf6'
        }

        self.root.configure(bg=self.colors['bg'])
        
        # Resolution presets
        self.resolutions = {
            "480P": {"landscape": (854, 480), "portrait": (480, 854)},
            "720P": {"landscape": (1280, 720), "portrait": (720, 1280)},
            "1080P": {"landscape": (1920, 1080), "portrait": (1080, 1920)},
            "2K": {"landscape": (2560, 1440), "portrait": (1440, 2560)},
            "4K": {"landscape": (3840, 2160), "portrait": (2160, 3840)}
        }
        
        self.folder_path = None
        self.image_files = []
        self.current_index = 0
        self.current_image = None
        self.output_folder = None

        # Default settings
        self.selected_resolution = "1080P"
        self.selected_orientation = "landscape"
        self.output_format = "JPEG"
        self.jpeg_quality = 85
        self.crop_x = 0
        self.crop_y = 0

        # Store button references
        self.res_buttons = {}
        self.orient_buttons = {}
        self.format_buttons = {}

        self.create_widgets()
        
    def create_widgets(self):
        # Main container with sidebar layout
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left Sidebar
        sidebar = tk.Frame(main_container, bg=self.colors['sidebar'], width=350)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Sidebar Header
        header_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(header_frame, text="Image Resizer Pro", 
                font=("Segoe UI", 18, "bold"), bg=self.colors['sidebar'], 
                fg='white').pack(anchor='w')
        tk.Label(header_frame, text="Professional batch image processing", 
                font=("Segoe UI", 9), bg=self.colors['sidebar'], 
                fg=self.colors['text_dim']).pack(anchor='w', pady=(5, 0))
        
        # Settings Container
        settings_container = tk.Frame(sidebar, bg=self.colors['sidebar'])
        settings_container.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Resolution Card (Dropdown)
        self.create_section_header(settings_container, "Resolution")
        res_card = self.create_card(settings_container)
        
        # Create custom styled dropdown
        self.resolution_var = tk.StringVar(value=self.selected_resolution)
        
        # Create a frame that looks like our other buttons
        dropdown_container = tk.Frame(res_card, bg=self.colors['bg'], 
                                     highlightbackground=self.colors['border'],
                                     highlightthickness=0)
        dropdown_container.pack(fill=tk.X, pady=5)
        
        self.resolution_menu = tk.OptionMenu(dropdown_container, self.resolution_var, 
                                            *self.resolutions.keys(),
                                            command=self.on_resolution_dropdown_change)
        
        # Style to match our dark theme buttons
        self.resolution_menu.config(
            bg=self.colors['bg'], 
            fg='white', 
            font=("Segoe UI", 11, "bold"),
            activebackground=self.colors['sidebar'],
            activeforeground='white',
            highlightthickness=0, 
            bd=0,
            relief=tk.FLAT, 
            padx=15, 
            pady=10,
            cursor='hand2',
            anchor='w',
            indicatoron=0,
            width=25
        )
        
        # Style the dropdown menu list
        menu = self.resolution_menu['menu']
        menu.config(
            bg=self.colors['card'], 
            fg='white', 
            activebackground=self.colors['primary'],
            activeforeground='white', 
            bd=0,
            relief=tk.FLAT,
            font=("Segoe UI", 10, "bold"),
            tearoff=0
        )
        
        # Add hover effect
        def on_enter(e):
            self.resolution_menu.config(bg=self.colors['sidebar'])
        
        def on_leave(e):
            self.resolution_menu.config(bg=self.colors['bg'])
        
        self.resolution_menu.bind('<Enter>', on_enter)
        self.resolution_menu.bind('<Leave>', on_leave)
        
        self.resolution_menu.pack(fill=tk.X)
        
        # Orientation Card
        self.create_section_header(settings_container, "Orientation", 15)
        orient_card = self.create_card(settings_container)
        
        orient_frame = tk.Frame(orient_card, bg=self.colors['card'])
        orient_frame.pack(fill=tk.X, pady=5)
        
        landscape_btn = ModernButton(orient_frame, "Landscape",
                                    lambda: self.on_orientation_change("landscape"),
                                    bg_color=self.colors['bg'],
                                    hover_color=self.colors['sidebar'],
                                    font_size=10, bold=True, width=140)
        landscape_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.orient_buttons['landscape'] = landscape_btn
        
        portrait_btn = ModernButton(orient_frame, "Portrait",
                                   lambda: self.on_orientation_change("portrait"),
                                   bg_color=self.colors['bg'],
                                   hover_color=self.colors['sidebar'],
                                   font_size=10, bold=True, width=140)
        portrait_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.orient_buttons['portrait'] = portrait_btn
        
        self.update_orientation_buttons()
        
        # Crop Adjustment Card
        self.create_section_header(settings_container, "Crop Position", 15)
        crop_card = self.create_card(settings_container)
        
        # Container for crop sliders (will show/hide based on orientation)
        self.crop_container = tk.Frame(crop_card, bg=self.colors['card'])
        self.crop_container.pack(fill=tk.X)
        
        # Horizontal crop
        self.h_frame = tk.Frame(self.crop_container, bg=self.colors['card'])
        
        h_label_frame = tk.Frame(self.h_frame, bg=self.colors['card'])
        h_label_frame.pack(fill=tk.X)
        tk.Label(h_label_frame, text="Horizontal", font=("Segoe UI", 9, "bold"), 
                bg=self.colors['card'], fg='white').pack(side=tk.LEFT)
        self.h_value_label = tk.Label(h_label_frame, text="0", font=("Segoe UI", 9), 
                bg=self.colors['card'], fg=self.colors['text_dim'])
        self.h_value_label.pack(side=tk.RIGHT)
        
        self.crop_x_scale = tk.Scale(self.h_frame, from_=-100, to=100, orient=tk.HORIZONTAL,
                                     command=self.on_crop_change, bg=self.colors['card'],
                                     fg='white', troughcolor=self.colors['bg'],
                                     highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                                     activebackground=self.colors['primary'],
                                     showvalue=0, font=("Segoe UI", 9))
        self.crop_x_scale.set(0)
        self.crop_x_scale.pack(fill=tk.X, pady=(5, 10))
        
        # Vertical crop
        self.v_frame = tk.Frame(self.crop_container, bg=self.colors['card'])
        
        v_label_frame = tk.Frame(self.v_frame, bg=self.colors['card'])
        v_label_frame.pack(fill=tk.X)
        tk.Label(v_label_frame, text="Vertical", font=("Segoe UI", 9, "bold"), 
                bg=self.colors['card'], fg='white').pack(side=tk.LEFT)
        self.v_value_label = tk.Label(v_label_frame, text="0", font=("Segoe UI", 9), 
                bg=self.colors['card'], fg=self.colors['text_dim'])
        self.v_value_label.pack(side=tk.RIGHT)
        
        self.crop_y_scale = tk.Scale(self.v_frame, from_=-100, to=100, orient=tk.HORIZONTAL,
                                     command=self.on_crop_change, bg=self.colors['card'],
                                     fg='white', troughcolor=self.colors['bg'],
                                     highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                                     activebackground=self.colors['primary'],
                                     showvalue=0, font=("Segoe UI", 9))
        self.crop_y_scale.set(0)
        self.crop_y_scale.pack(fill=tk.X, pady=(5, 10))
        
        # Show appropriate slider based on orientation
        self.update_crop_sliders()
        
        # Reset button
        reset_btn = ModernButton(crop_card, "Reset to Center", self.reset_crop,
                                bg_color=self.colors['bg'],
                                hover_color=self.colors['sidebar'],
                                font_size=10, bold=False)
        reset_btn.pack(fill=tk.X, pady=(5, 5))
        
        # Output Format Card
        self.create_section_header(settings_container, "Output Format", 15)
        format_card = self.create_card(settings_container)
        
        format_frame = tk.Frame(format_card, bg=self.colors['card'])
        format_frame.pack(fill=tk.X, pady=5)
        
        jpeg_btn = ModernButton(format_frame, "JPEG",
                               lambda: self.on_format_change("JPEG"),
                               bg_color=self.colors['bg'],
                               hover_color=self.colors['sidebar'],
                               font_size=10, bold=True, width=90)
        jpeg_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3))
        self.format_buttons['JPEG'] = jpeg_btn
        
        png_btn = ModernButton(format_frame, "PNG",
                              lambda: self.on_format_change("PNG"),
                              bg_color=self.colors['bg'],
                              hover_color=self.colors['sidebar'],
                              font_size=10, bold=True, width=90)
        png_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(3, 3))
        self.format_buttons['PNG'] = png_btn
        
        webp_btn = ModernButton(format_frame, "WEBP",
                               lambda: self.on_format_change("WEBP"),
                               bg_color=self.colors['bg'],
                               hover_color=self.colors['sidebar'],
                               font_size=10, bold=True, width=90)
        webp_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(3, 0))
        self.format_buttons['WEBP'] = webp_btn
        
        # JPEG Quality slider (shown only for JPEG)
        self.quality_frame = tk.Frame(format_card, bg=self.colors['card'])
        
        q_label_frame = tk.Frame(self.quality_frame, bg=self.colors['card'])
        q_label_frame.pack(fill=tk.X, pady=(10, 0))
        tk.Label(q_label_frame, text="JPEG Quality", font=("Segoe UI", 9, "bold"), 
                bg=self.colors['card'], fg='white').pack(side=tk.LEFT)
        self.quality_value_label = tk.Label(q_label_frame, text=str(self.jpeg_quality), 
                                           font=("Segoe UI", 9), 
                                           bg=self.colors['card'], fg=self.colors['text_dim'])
        self.quality_value_label.pack(side=tk.RIGHT)
        
        self.quality_scale = tk.Scale(self.quality_frame, from_=1, to=100, orient=tk.HORIZONTAL,
                                     command=self.on_quality_change, bg=self.colors['card'],
                                     fg='white', troughcolor=self.colors['bg'],
                                     highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                                     activebackground=self.colors['primary'],
                                     showvalue=0, font=("Segoe UI", 9))
        self.quality_scale.set(self.jpeg_quality)
        self.quality_scale.pack(fill=tk.X, pady=(5, 0))
        
        self.update_format_buttons()
        
        # Right Content Area
        content_area = tk.Frame(main_container, bg=self.colors['bg'])
        content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Top bar with info
        top_bar = tk.Frame(content_area, bg=self.colors['card'], height=60)
        top_bar.pack(fill=tk.X, padx=20, pady=(20, 10))
        top_bar.pack_propagate(False)
        
        self.info_label = tk.Label(top_bar, text="", font=("Segoe UI", 10), 
                                   bg=self.colors['card'], fg='white',
                                   anchor='w', padx=20)
        self.info_label.pack(fill=tk.BOTH, expand=True)
        
        # Image preview area
        preview_container = tk.Frame(content_area, bg=self.colors['bg'])
        preview_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        self.canvas_frame = tk.Frame(preview_container, bg=self.colors['card'],
                                     highlightbackground=self.colors['border'],
                                     highlightthickness=1)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg=self.colors['bg'],
                               highlightthickness=0, bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        # Small preview of uncropped image (top right corner)
        self.preview_overlay_frame = tk.Frame(self.canvas, bg=self.colors['card'],
                                             highlightbackground=self.colors['primary'],
                                             highlightthickness=2)

        # Header for the preview
        preview_header = tk.Frame(self.preview_overlay_frame, bg=self.colors['sidebar'], height=25)
        preview_header.pack(fill=tk.X)
        preview_header.pack_propagate(False)

        tk.Label(preview_header, text="Original (Uncropped)",
                font=("Segoe UI", 9, "bold"), bg=self.colors['sidebar'],
                fg='white', padx=8).pack(side=tk.LEFT, fill=tk.Y)

        # Canvas for the small preview
        self.preview_canvas = tk.Canvas(self.preview_overlay_frame,
                                       bg=self.colors['bg'],
                                       width=200, height=150,
                                       highlightthickness=0, bd=0)
        self.preview_canvas.pack(padx=2, pady=2)

        # Initially hidden
        self.preview_overlay_frame.place_forget()

        # Welcome screen (shown when no folder is selected)
        self.welcome_frame = tk.Frame(self.canvas, bg=self.colors['bg'])

        welcome_content = tk.Frame(self.welcome_frame, bg=self.colors['bg'])
        welcome_content.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(welcome_content, text="🖼️", font=("Segoe UI", 72),
                bg=self.colors['bg'], fg=self.colors['primary']).pack(pady=(0, 20))

        tk.Label(welcome_content, text="Welcome to Image Resizer Pro",
                font=("Segoe UI", 24, "bold"), bg=self.colors['bg'],
                fg='white').pack(pady=(0, 10))

        tk.Label(welcome_content, text="Select a folder to get started",
                font=("Segoe UI", 12), bg=self.colors['bg'],
                fg=self.colors['text_dim']).pack(pady=(0, 30))

        select_folder_btn = ModernButton(welcome_content, "📁 Select Folder",
                                        self.select_folder,
                                        bg_color=self.colors['primary'],
                                        hover_color=self.colors['primary_hover'],
                                        font_size=16, bold=True, width=250, height=60)
        select_folder_btn.pack()

        # Show welcome screen initially
        self.show_welcome_screen()
        
        # Bottom action bar
        action_bar = tk.Frame(content_area, bg=self.colors['bg'], height=80)
        action_bar.pack(fill=tk.X, padx=20, pady=(0, 20))
        action_bar.pack_propagate(False)
        
        btn_container = tk.Frame(action_bar, bg=self.colors['bg'])
        btn_container.pack(expand=True)
        
        # Navigation buttons with modern style
        prev_btn = ModernButton(btn_container, "← Previous", self.previous_image,
                               bg_color=self.colors['bg'],
                               hover_color=self.colors['sidebar'],
                               font_size=14, bold=True, width=150)
        prev_btn.pack(side=tk.LEFT, padx=5)
        
        skip_btn = ModernButton(btn_container, "Skip →", self.skip_image,
                               bg_color=self.colors['bg'],
                               hover_color=self.colors['sidebar'],
                               font_size=14, bold=True, width=150)
        skip_btn.pack(side=tk.LEFT, padx=5)
        
        process_btn = ModernButton(btn_container, "✓ Process & Next", self.process_and_next,
                                  bg_color=self.colors['primary'],
                                  hover_color=self.colors['primary_hover'],
                                  font_size=16, bold=True, width=200, height=50)
        process_btn.pack(side=tk.LEFT, padx=5)
        
        batch_btn = ModernButton(btn_container, "⚡ Process All", self.process_all,
                                bg_color=self.colors['accent'],
                                hover_color='#7c3aed',
                                font_size=14, bold=True, width=180)
        batch_btn.pack(side=tk.LEFT, padx=5)
        
    def create_section_header(self, parent, text, top_pad=20):
        tk.Label(parent, text=text, font=("Segoe UI", 11, "bold"), 
                bg=self.colors['sidebar'], fg='white').pack(anchor='w', pady=(top_pad, 8))
    
    def create_card(self, parent):
        card = tk.Frame(parent, bg=self.colors['card'], highlightbackground=self.colors['border'],
                       highlightthickness=1)
        card.pack(fill=tk.X, pady=(0, 5))
        
        inner = tk.Frame(card, bg=self.colors['card'])
        inner.pack(fill=tk.BOTH, padx=12, pady=12)
        return inner
    
    def on_resolution_change(self, resolution):
        self.selected_resolution = resolution
        self.display_preview()
        self.update_info()
    
    def on_resolution_dropdown_change(self, resolution):
        self.selected_resolution = resolution
        self.display_preview()
        self.update_info()
    
    def update_resolution_buttons(self):
        for res, btn in self.res_buttons.items():
            if res == self.selected_resolution:
                btn.set_bg(self.colors['primary'])
                btn.hover_color = self.colors['primary_hover']
            else:
                btn.set_bg(self.colors['bg'])
                btn.hover_color = self.colors['sidebar']
    
    def on_orientation_change(self, orientation):
        self.selected_orientation = orientation
        self.update_orientation_buttons()
        self.update_crop_sliders()
        self.display_preview()
        self.update_info()
    
    def update_orientation_buttons(self):
        for orient, btn in self.orient_buttons.items():
            if orient == self.selected_orientation:
                btn.set_bg(self.colors['primary'])
                btn.hover_color = self.colors['primary_hover']
            else:
                btn.set_bg(self.colors['bg'])
                btn.hover_color = self.colors['sidebar']
    
    def update_crop_sliders(self):
        """Show only relevant crop slider based on orientation"""
        # Hide both first
        self.h_frame.pack_forget()
        self.v_frame.pack_forget()
        
        # Show the relevant one
        if self.selected_orientation == "landscape":
            # For landscape, only show vertical crop (top/bottom)
            self.v_frame.pack(fill=tk.X, pady=(5, 10))
        else:
            # For portrait, only show horizontal crop (left/right)
            self.h_frame.pack(fill=tk.X, pady=(5, 10))
    
    def on_format_change(self, format_type):
        self.output_format = format_type
        self.update_format_buttons()
        self.update_info()
    
    def update_format_buttons(self):
        for fmt, btn in self.format_buttons.items():
            if fmt == self.output_format:
                btn.set_bg(self.colors['primary'])
                btn.hover_color = self.colors['primary_hover']
            else:
                btn.set_bg(self.colors['bg'])
                btn.hover_color = self.colors['sidebar']
        
        # Show/hide JPEG quality slider
        if self.output_format == "JPEG":
            self.quality_frame.pack(fill=tk.X, pady=(5, 5))
        else:
            self.quality_frame.pack_forget()
    
    def on_quality_change(self, val):
        self.jpeg_quality = int(float(val))
        self.quality_value_label.config(text=str(self.jpeg_quality))
        self.update_info()

    def show_welcome_screen(self):
        """Show the welcome screen"""
        self.welcome_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def hide_welcome_screen(self):
        """Hide the welcome screen"""
        self.welcome_frame.place_forget()

    def reset_to_welcome(self):
        """Reset the app state and return to welcome screen"""
        # Clear current state
        self.folder_path = None
        self.image_files = []
        self.current_index = 0
        self.current_image = None
        self.output_folder = None

        # Clear the canvas
        self.canvas.delete("all")

        # Hide the preview overlay
        self.preview_overlay_frame.place_forget()

        # Clear info label
        self.info_label.config(text="")

        # Show welcome screen
        self.show_welcome_screen()

    def select_folder(self):
        # Bring window to front before showing dialog
        self.root.lift()
        self.root.focus_force()

        self.folder_path = filedialog.askdirectory(title="Select Folder with Images")
        if not self.folder_path:
            # User cancelled - just return without quitting
            return

        # Get all image files
        extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')
        self.image_files = [f for f in os.listdir(self.folder_path)
                           if f.lower().endswith(extensions)]
        self.image_files.sort()

        if not self.image_files:
            messagebox.showerror("No Images", "No images found in the selected folder.")
            return

        # Create output folder
        self.output_folder = os.path.join(self.folder_path, "SSResized")
        os.makedirs(self.output_folder, exist_ok=True)

        # Hide welcome screen and show first image
        self.hide_welcome_screen()
        self.current_index = 0
        self.load_image()
        
    def load_image(self):
        if self.current_index >= len(self.image_files):
            messagebox.showinfo("Complete", "All images have been processed!")
            self.reset_to_welcome()
            return

        img_path = os.path.join(self.folder_path, self.image_files[self.current_index])
        self.current_image = Image.open(img_path)
        self.display_preview()
        self.update_info()
        
    def display_preview(self):
        if not self.current_image:
            return
        
        # Get target resolution
        target_width, target_height = self.get_target_resolution()
        
        # Calculate crop
        cropped = self.get_cropped_image()
        
        # Resize to target
        resized = cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Scale for display
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 960
            canvas_height = 540
        
        img_ratio = resized.width / resized.height
        canvas_ratio = canvas_width / canvas_height
        
        if img_ratio > canvas_ratio:
            display_width = canvas_width
            display_height = int(canvas_width / img_ratio)
        else:
            display_height = canvas_height
            display_width = int(canvas_height * img_ratio)
        
        display_image = resized.resize((display_width, display_height), Image.Resampling.LANCZOS)
        
        self.photo = ImageTk.PhotoImage(display_image)
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.photo, anchor=tk.CENTER)

        # Update the small uncropped preview
        self.update_uncropped_preview()

    def update_uncropped_preview(self):
        """Display a small preview of the uncropped original image"""
        if not self.current_image:
            self.preview_overlay_frame.place_forget()
            return

        # Show the preview overlay
        self.preview_overlay_frame.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)

        # Create a small version of the original image
        preview_width = 200
        preview_height = 150

        # Calculate scaling to fit in preview box
        img_width, img_height = self.current_image.size
        img_ratio = img_width / img_height
        preview_ratio = preview_width / preview_height

        if img_ratio > preview_ratio:
            # Image is wider
            small_width = preview_width
            small_height = int(preview_width / img_ratio)
        else:
            # Image is taller
            small_height = preview_height
            small_width = int(preview_height * img_ratio)

        small_image = self.current_image.resize((small_width, small_height), Image.Resampling.LANCZOS)

        # Draw the crop area rectangle on the preview
        # Calculate what portion is being cropped
        target_width, target_height = self.get_target_resolution()
        target_ratio = target_width / target_height

        if img_ratio > target_ratio:
            # Cropping width
            new_width = int(img_height * target_ratio)
            new_height = img_height
        else:
            # Cropping height
            new_width = img_width
            new_height = int(img_width / target_ratio)

        # Apply crop offset
        x_offset = int((img_width - new_width) / 2 * (1 + self.crop_x / 100))
        y_offset = int((img_height - new_height) / 2 * (1 + self.crop_y / 100))
        x_offset = max(0, min(x_offset, img_width - new_width))
        y_offset = max(0, min(y_offset, img_height - new_height))

        # Convert to preview coordinates
        scale_x = small_width / img_width
        scale_y = small_height / img_height

        rect_x1 = x_offset * scale_x
        rect_y1 = y_offset * scale_y
        rect_x2 = (x_offset + new_width) * scale_x
        rect_y2 = (y_offset + new_height) * scale_y

        # Create the preview with rectangle overlay
        self.preview_photo = ImageTk.PhotoImage(small_image)
        self.preview_canvas.delete("all")

        # Center the image in the preview canvas
        canvas_center_x = preview_width // 2
        canvas_center_y = preview_height // 2

        self.preview_canvas.create_image(canvas_center_x, canvas_center_y,
                                        image=self.preview_photo, anchor=tk.CENTER)

        # Draw the crop rectangle
        offset_x = (preview_width - small_width) // 2
        offset_y = (preview_height - small_height) // 2

        self.preview_canvas.create_rectangle(
            offset_x + rect_x1, offset_y + rect_y1,
            offset_x + rect_x2, offset_y + rect_y2,
            outline=self.colors['primary'], width=2
        )

        # Add semi-transparent overlay for cropped-out areas
        # Top
        if rect_y1 > 0:
            self.preview_canvas.create_rectangle(
                offset_x, offset_y,
                offset_x + small_width, offset_y + rect_y1,
                fill='black', stipple='gray50', outline=''
            )
        # Bottom
        if rect_y2 < small_height:
            self.preview_canvas.create_rectangle(
                offset_x, offset_y + rect_y2,
                offset_x + small_width, offset_y + small_height,
                fill='black', stipple='gray50', outline=''
            )
        # Left
        if rect_x1 > 0:
            self.preview_canvas.create_rectangle(
                offset_x, offset_y + rect_y1,
                offset_x + rect_x1, offset_y + rect_y2,
                fill='black', stipple='gray50', outline=''
            )
        # Right
        if rect_x2 < small_width:
            self.preview_canvas.create_rectangle(
                offset_x + rect_x2, offset_y + rect_y1,
                offset_x + small_width, offset_y + rect_y2,
                fill='black', stipple='gray50', outline=''
            )

    def get_target_resolution(self):
        return self.resolutions[self.selected_resolution][self.selected_orientation]
        
    def get_cropped_image(self):
        target_width, target_height = self.get_target_resolution()
        target_ratio = target_width / target_height
        
        img_width, img_height = self.current_image.size
        img_ratio = img_width / img_height
        
        if img_ratio > target_ratio:
            # Image is wider, crop width
            new_width = int(img_height * target_ratio)
            new_height = img_height
        else:
            # Image is taller, crop height
            new_width = img_width
            new_height = int(img_width / target_ratio)
        
        # Apply crop offset (percentage of available crop space)
        x_offset = int((img_width - new_width) / 2 * (1 + self.crop_x / 100))
        y_offset = int((img_height - new_height) / 2 * (1 + self.crop_y / 100))
        
        # Ensure crop stays within bounds
        x_offset = max(0, min(x_offset, img_width - new_width))
        y_offset = max(0, min(y_offset, img_height - new_height))
        
        return self.current_image.crop((x_offset, y_offset, x_offset + new_width, y_offset + new_height))
        
    def on_crop_change(self, val):
        self.crop_x = self.crop_x_scale.get()
        self.crop_y = self.crop_y_scale.get()
        self.h_value_label.config(text=str(self.crop_x))
        self.v_value_label.config(text=str(self.crop_y))
        self.display_preview()
        
    def reset_crop(self):
        self.crop_x_scale.set(0)
        self.crop_y_scale.set(0)
        self.crop_x = 0
        self.crop_y = 0
        self.display_preview()
        
    def update_info(self):
        # Don't update info if no folder is selected yet
        if not self.folder_path or not self.image_files or not self.current_image:
            self.info_label.config(text="")
            return

        info = f"📁 Image {self.current_index + 1}/{len(self.image_files)}  •  "
        info += f"📄 {self.image_files[self.current_index]}  •  "
        info += f"Original: {self.current_image.size[0]}×{self.current_image.size[1]}  •  "
        target = self.get_target_resolution()
        info += f"Output: {target[0]}×{target[1]}  •  "

        # Calculate estimated file size
        estimated_size = self.estimate_output_size()
        info += f"Est. Size: {estimated_size}"

        self.info_label.config(text=info)
    
    def estimate_output_size(self):
        """Estimate output file size based on resolution and format by actually encoding the image"""
        if not self.current_image:
            return "N/A"

        try:
            # Get the processed image (cropped and resized)
            target_width, target_height = self.get_target_resolution()
            cropped = self.get_cropped_image()
            resized = cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)

            # Save to memory buffer to get actual size
            buffer = BytesIO()

            if self.output_format == "JPEG":
                # Convert to RGB if necessary (JPEG doesn't support transparency)
                if resized.mode in ('RGBA', 'LA', 'P'):
                    rgb_image = Image.new('RGB', resized.size, (255, 255, 255))
                    if resized.mode == 'P':
                        resized = resized.convert('RGBA')
                    rgb_image.paste(resized, mask=resized.split()[-1] if resized.mode in ('RGBA', 'LA') else None)
                    resized = rgb_image
                resized.save(buffer, format='JPEG', quality=self.jpeg_quality, optimize=True)
            elif self.output_format == "PNG":
                resized.save(buffer, format='PNG', optimize=True)
            else:  # WEBP
                resized.save(buffer, format='WEBP', quality=85)

            # Get the size in bytes
            estimated_bytes = buffer.tell()

            # Convert to human-readable format
            if estimated_bytes < 1024:
                return f"{estimated_bytes:.0f} B"
            elif estimated_bytes < 1024 * 1024:
                return f"{estimated_bytes / 1024:.1f} KB"
            else:
                return f"{estimated_bytes / (1024 * 1024):.2f} MB"
        except Exception as e:
            return "N/A"
        
    def process_current_image(self):
        target_width, target_height = self.get_target_resolution()
        cropped = self.get_cropped_image()
        resized = cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Get file extension based on format
        original_name = os.path.splitext(self.image_files[self.current_index])[0]
        if self.output_format == "JPEG":
            output_filename = f"{original_name}.jpg"
        elif self.output_format == "PNG":
            output_filename = f"{original_name}.png"
        else:  # WEBP
            output_filename = f"{original_name}.webp"
        
        output_path = os.path.join(self.output_folder, output_filename)
        
        # Save with appropriate format and settings
        if self.output_format == "JPEG":
            resized.save(output_path, format='JPEG', quality=self.jpeg_quality, optimize=True)
        elif self.output_format == "PNG":
            resized.save(output_path, format='PNG', optimize=True)
        else:  # WEBP
            resized.save(output_path, format='WEBP', quality=85)
        
    def process_and_next(self):
        self.process_current_image()
        self.current_index += 1
        self.load_image()
        
    def skip_image(self):
        self.current_index += 1
        self.load_image()
        
    def previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_image()
        else:
            messagebox.showinfo("First Image", "This is the first image.")
            
    def process_all(self):
        result = messagebox.askyesno("Confirm",
            f"Process all remaining {len(self.image_files) - self.current_index} images with current settings?")
        if result:
            while self.current_index < len(self.image_files):
                self.process_current_image()
                self.current_index += 1
            messagebox.showinfo("Complete", "All images processed!")
            self.reset_to_welcome()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()