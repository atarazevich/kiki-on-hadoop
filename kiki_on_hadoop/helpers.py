import sys
import optparse
import yaml

def get_configurations(section_name='kiki'):
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config", dest="config_file",
        help="Full path to configuration file for Kiki", metavar="FILE",
        default='/etc/kiki/kiki.yaml'
    )
    options, _ = parser.parse_args()

    try:
        config_file = open(options.config_file)
    except IOError:
        sys.exit('Unable to find config file: '+ options.config_file)

    return yaml.load(config_file).get(section_name, {})