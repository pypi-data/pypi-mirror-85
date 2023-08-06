import research_jupyter_templates
import os.path
import shutil
import glob


for file in glob.glob(os.path.join(research_jupyter_templates.path,'*.ipynb'):
    
    site_packages_path,_ = os.path.split(research_jupyter_templates.path)

    dest_dir = os.path.join(site_packages_path,'jupyterlab_templates','templates','jupyterlab_templates')

    print('Copy %s to %s' %(file,dest_dir))

    shutil.copy(file, dest_dir)
