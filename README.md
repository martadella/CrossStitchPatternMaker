# CrossStitchPatternMaker
Converts an image to a cross stitch pattern based on user-specified width of the final pattern and the number of colors used.
Draws vertical and horizontal lines, creating cells, and assigns a character to each cell.

Installation:

Go to your project directory and create virtual environment:

virtualenv --python=python3 venv

Activate virtual environment:

. venv/bin/activate

Install required modules:

pip install image

pip install scikit-image

pip install -U scikit-learn


Run the application:

python cross_stitch.py image_to_be_cross_stitched.JPG -w 100 -c 10

Be patient! The process may take a while.
