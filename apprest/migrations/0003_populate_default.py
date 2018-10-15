from django.db import migrations, transaction


from apprest.models.facility import CalipsoFacility
from apprest.models.image import CalipsoAvailableImages



def create_image_default(apps, schema_editor):
    default_data_image=[
        ('base_image', 'tcp://calipsotest.cells.es:2375', 'consol/centos-xfce-vnc:latest', 1, '3G', '5G'),
        ('base_jupyter', 'tcp://calipsotest.cells.es:2375', 'jupyter/scipy-notebook', 1, '3G', '5G')]

    for image_data in default_data_image:
        public_name = image_data[0]
        docker_daemon = image_data[1]
        image = image_data[2]
        cpu = image_data[3]
        memory = image_data[4]
        hdd = image_data[5]
        try:
            CalipsoAvailableImages.objects.create(public_name=public_name,docker_daemon=docker_daemon,image=image,cpu=cpu,memory=memory,hdd=hdd)
        except Exception as e:
            print('Error creating image_default: %s' % e)


def create_facilities_default(apps, schema_editor):
    default_facilities=[ ('ALBA Light Source', 'ALBA is a 3rd generation Synchrotron Light facility located in Cerdanyola del Vallès, (Barcelona), being the newest source in the Mediterranean area. It is a complex of electron accelerators to produce synchrotron light, which allows the visualization of the atomic structure of matter as well as the study of its properties.  The 3 GeV electron beam energy at ALBA is achieved by combining a LInear ACcelerator (LINAC) and a low-emittance, full-energy BOOSTER placed in the same tunnel as the STORAGE RING. ALBA\'s 270 meter perimeter has 17 straight sections all of which are available for the installation of insertion devices.', 'http://calipsoplus.cells.es'),
                        ('Diamond Light Source', 'Diamond Light Source is the UK’s national synchrotron. It works like a giant microscope, harnessing the power of electrons to produce bright light that scientists can use to study anything from fossils to jet engines to viruses and vaccines. The machine accelerates electrons to near light speeds so that they give off light 10 billion times brighter than the sun. These bright beams are then directed off into laboratories known as ‘beamlines’. Here, scientists use the light to study a vast range of subject matter, from new medicines and treatments for disease to innovative engineering and cutting-edge technology.', 'http://www.diamond.ac.uk'),
                        ('Elettra and FERMI Lightsource', 'Elettra Sincrotrone Trieste is a multidisciplinary international research center of excellence, specialized in generating high quality synchrotron and free-electron laser light and applying it in materials and life sciences. Its mission is to promote cultural, social and economic growth through: Basic and applied research; Technology and know-how transfer; Technical, scientific and management education; Role of reference in the national and international scientific networks. ', 'https://www.elettra.trieste.it/'),
                        ('Helmholz-Zentrum Berlin (HZB)', 'Energy materials comprise more than just solar cells. Energy materials also include solar fuels, thermoelectrics, and topological insulators. These are materials that store or convert energy, or enable construction of new energy-efficient information technologies like spintronics. Scientists at HZB are researching these kinds of systems of materials, always with the emphasis on thin-film technologies. We are able to build on the know-how we already acquired in the area of thin-film photovoltaics and that HZB research is known for internationally. Now we are combining the outstanding means of analysis offered in particular at BESSY II and BER II with expanded expertise in materials synthesis, as well as in the field of simulation and theory. Especially interesting research advances at HZB are presented in our annual reports and highlights and through our Research Highlights web pages. You can learn more about the research programmes\"', ' scientific institutes'),
                        ('European Synchrotron Radiation Facility', 'The ESRF is the world\'s most intense X-ray source and a centre of excellence for fundamental and innovation-driven research in condensed and living matter science. Located in Grenoble, France, the ESRF owes its success to the international cooperation of 22 partner nations, of which 13 are Members and 9 are Associates.', 'http://www.esrf.eu'),
                        ('European XFEL', 'The European XFEL is a research facility of superlatives: It generates ultrashort X-ray flashes—27 000 times per second and with a brilliance that is a billion times higher than that of the best conventional X-ray radiation sources.', 'https://www.xfel.eu/'),
                        ('DESY', 'DESY is one of the world’s leading accelerator centres. Researchers use the large-scale facilities at DESY to explore the microcosm in all its variety – from the interactions of tiny elementary particles and the behaviour of new types of nanomaterials to biomolecular processes that are essential to life. The accelerators and detectors that DESY develops and builds are unique research tools. The facilities generate the world’s most intense X-ray light, accelerate particles to record energies and open completely new windows onto the universe. ?That makes DESY not only a magnet for more than 3000 guest researchers from over 40 countries every year, but also a coveted partner for national and international cooperations. Committed young researchers find an exciting interdisciplinary setting at DESY. The research centre offers specialized training for a large number of professions. DESY cooperates with industry and business to promote new technologies that will benefit society and encourage innovations. This also benefits the metropolitan regions of the two DESY locations, Hamburg and Zeuthen near Berlin.', 'http://www.desy.de/'),
                        ('Soleil Synchrotron', 'High-technology facility, SOLEIL is both an electromagnetic radiation source covering a wide range of energies (from the infrared to the x-rays) and a research laboratory at the cutting edge of experimental techniques dedicated to matter analysis down to the atomic scale, as well as a service platform open to all scientific and industrial communities.', 'https://www.synchrotron-soleil.fr/'),
                        ('Paul Scherrer Institute', 'The Paul Scherrer Institute, PSI, is the largest research institute for natural and engineering sciences within Switzerland. We perform world-class research in three main subject areas: Matter and Material; Energy and the Environment; and Human Health. By conducting fundamental and applied research, we work on long-term solutions for major challenges facing society, industry and science.', 'https://www.psi.ch/'),
                        ('University of Lund', 'Lund is the most popular study location in Sweden. The University offers one of the broadest ranges of programmes and courses in Scandinavia, based on cross-disciplinary and cutting-edge research. The University has a distinct international profile, with partner universities in over 70 countries.', 'https://www.lunduniversity.lu.se/')]
    for facility in default_facilities:
        name = facility[0]
        description = facility[1]
        url = facility[2]
        try:
            CalipsoFacility.objects.create(name=name,description=description,url=url)
        except Exception as e:
            print('Error creating facility_default: %s' % e)


class Migration(migrations.Migration):
    dependencies = [
        ('apprest', '0002_auto_20180720_1511'),
    ]
    
    operations = [migrations.RunPython(create_image_default), migrations.RunPython(create_facilities_default)]
