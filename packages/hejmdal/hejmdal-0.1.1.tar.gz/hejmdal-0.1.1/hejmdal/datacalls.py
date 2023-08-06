from .base import *
import sqlalchemy as db
import sqlalchemy.orm as orm
from sqlalchemy.sql import and_, or_, not_
import pandas as pd
import json
import numpy as np
import decimal
import datetime
import os
import requests
import io

class TableMetaData:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return f"{self.__class__}({self.__dict__})"

    def to_json(self):
        return json.dumps(self.__dict__)

    def to_dict(self):
        return self.__dict__
  
class Data:
    def __init__(self, request):
        self.request = request
        self.build()
        
    def build(self):
        self.data = self.get_data()
        self.data_out = self.interpret_data()

    def get_data(self):
        return {}
        
    def interpret_data(self):
        return self.data
      
def load_pandas(connection, sql):
    logger = get_logger()
    logger.debug(f"calling sql string:{sql}")
    query = connection.execute(sql)
    result = pd.DataFrame(query.fetchall())
    if len(result) < 1: raise EmptyResult()
    result.columns = query.keys()
    logger.debug(f"sql resulted in {len(result)} rows and {', '.join(result.columns)} as columns")
    return result


class DatabaseResult(Data):
    def __init__(self, request, database=None):
        self.logger = get_logger() # ensure that logger have been generated, so we can refere to it as just logger
        self.database = database
        super().__init__(request)
        # self.request = request
        # self.data = self.request_data()
        # self.data_out = self.processing_step()

    def get_connection(self):
        with open('access.txt','r') as f:
            readline = lambda : ''.join(filter(lambda c: c!='\n',f.readline()))
            hosting = readline()
            username = readline()
            password = readline()
        passwordpart = f':{password}' if password else ''
        engine = db.create_engine(f'mysql+pymysql://{username}{passwordpart}@{hosting}')
        return engine.begin()
        
    def get_data(self):
        return self.request_data()
        
    def interpret_data(self):
        return self.processing_step()
        
    def request_data(self):
        return {}
        
    def processing_step(self):
        return self.data


class LocationData(DatabaseResult):
    def request_data(self):
        with self.get_connection() as connection:
            return {'locations': load_pandas(connection, "SELECT `display_name_IAGA_code` AS `IAGA Code`, `display_name_short` AS `short name`, `display_name_long` AS `long name`, `contact` FROM location_info")}

    
class MainData(DatabaseResult):
    def to_dict(self):
        return self.data

    def split_location(self, location):
        def at_location(reference):
            base_data = self.data[reference]
            return base_data[base_data['iaga_code'] == location]
        # TODO: add in sub location division
        return {'data':at_location('main'), 'baseline':at_location('baseline'), 'meta':at_location('meta'), 'scale':at_location('scale')}

    def validate(self, info):

        # validate the tables against each other

        # cycle through config ids
        for this_config_id, config_df_masked_by_config_id in info['meta'].groupby(level=0):

            # create masks with the data for just this config_id
            data_df_masked_by_config_id = info['data'].query(f"config_id == {this_config_id}")
            baseline_df_masked_by_config_id = info['baseline'].query(f"config_id == {this_config_id}")
            scale_df_masked_by_config_id = info['scale'].query(f"config_id == {this_config_id}")

            # validate
            # the metadata table is our core. We check everything else against it.
            # the data, baseline, and scale tables need to be checked for valid data when cycling through the config_ids in the metadata table

            # check the number of data channels we expect
            number_of_channels = config_df_masked_by_config_id['number_of_channels'].iloc[0]

            # check the the number of channels are in the scale table
            try:
                # check the number of channels found in the scale table against the expected number of channels
                # check that we have expected number of channel keys
                channels_in_scale_table = scale_df_masked_by_config_id.loc[this_config_id]['channel_key']
                if len(channels_in_scale_table) != number_of_channels:
                    raise ValidationFailure(f'Number of channel_key entries ({len(channels_in_scale_table)}) do not match number of channels in metadata ({number_of_channels}).')

                # pull out the channel ids we care about from the channel keys
                channel_ids = tuple(scale_df_masked_by_config_id.loc[this_config_id]['channel_key'].keys())

                # check that we have expected number of correction scale values
                channels_in_scale_table = scale_df_masked_by_config_id.loc[this_config_id]['correction_scale_value']
                if set(channel_ids).issubset(channels_in_scale_table):
                    raise ValidationFailure(f'Number of correction_scale_value entries ({channels_in_scale_table}) do not match number of channels in metadata ({channel_ids}).')
                # check that we have expected number of correction offset values
                channels_in_scale_table = scale_df_masked_by_config_id.loc[this_config_id]['offset_value']
                if set(channel_ids).issubset(channels_in_scale_table):
                    raise ValidationFailure(f'Number of offset_scale_value entries ({channels_in_scale_table}) do not match number of channels in metadata ({channel_ids}).')
            except Exception as ex:                
                self.logger.info(f"Exception validating number of channels in scale table")
                raise

            # each config ID has a pillar ID that must be in the baseline table       
            try:
                # pull the pillar id (there should be one)
                this_pillar_id = config_df_masked_by_config_id['pillar_id'].iloc[0]
                # check the number of pillar ids we have found in the baseline table (there should be at least 1)
                pillar_id_check = len(baseline_df_masked_by_config_id.loc[this_pillar_id])
                if pillar_id_check < 1:
                    raise ValidationFailure(f"No entires for pillar_id {this_pillar_id} found in baseline table.")
            except Exception as ex:
                self.logger.info(f"Exception validating pillar ID from baseline table")
                raise

            # each config ID has an associated number of channels. check we can find each one in the data table
            try:
                # check if the config_id is in the data table
                if this_config_id not in data_df_masked_by_config_id.index:
                    #TODO raise and exception here, back out gently
                    # raise ValidationFailure(f"No entires for config_id {this_config_id} found in data table.")
                    self.logger.info(f"No entires for config_id {this_config_id} found in data table.")
                    continue

                # pull out the channel ids we care about from the channel keys
                channel_ids = tuple(scale_df_masked_by_config_id.loc[this_config_id]['channel_key'].keys())

                # pull out the names of the outer level columns (data, quality, flag)
                outer_level_columns = tuple(info['data'].loc[this_config_id].columns.unique(level=0))

                # check that we have expected number of data channels
                for this_channel_id in channel_ids:
                    for this_outer_column in outer_level_columns:
                        channels_in_data_table = this_channel_id in info['data'].loc[this_config_id][this_outer_column].columns
                        if not channels_in_data_table:
                            raise ValidationFailure(f'Number of {this_outer_column} channel entries ({len(channels_in_data_table)}) do not match number of channels in metadata ({number_of_channels}).')

            except Exception as ex:
                self.logger.info(f"Exception validating number of channels in data table")
                raise

        # we have now validated all the data we care about to see if it is even in the dataframe at all.
        # note that it can still be missing, but now we know it was at least allocated
        # if there was a problem, this should throw, otherwise fine. No returns needed.

    def apply_baseline(self, info):

        # add new columns based on request
        if self.request.orientation() == "HDZ":
            info['data'] = info['data'].reindex(columns=info['data'].columns.tolist() + [('processed_data', 'h'),
                                                                                         ('processed_data', 'd'),
                                                                                         ('processed_data', 'z'),
                                                                                         ('processed_data', 'f')])

        # cycle through config ids
        for this_config_id, config_df_masked_by_config_id in info['meta'].groupby(level=0):

            # create masks with the data for just this config_id
            if this_config_id not in info['data'].index.get_level_values('config_id'):
                self.logger.debug(f"Config ID {this_config_id} not found in data dataframe.")
                continue
            if this_config_id not in info['scale'].index.values:
                self.logger.debug(f"Config ID {this_config_id} not found in scale dataframe.")
                continue
            if not info['baseline']['config_id'].isin([this_config_id]).any():
                self.logger.debug(f"Config ID {this_config_id} not found in baseline dataframe.")
                continue
            data_df_masked_by_config_id = info['data'].loc[this_config_id, :]
            baseline_df_masked_by_config_id = info['baseline'].loc[info['baseline']['config_id'] == this_config_id]
            scale_df_masked_by_config_id = info['scale'].loc[this_config_id, :]

            # next, determine which channels correspond to which direction
            channels_keys_dict = scale_df_masked_by_config_id['channel_key'].to_dict()

            # the channel keys determine everything else, so we use them as the root and rename everything else
            required_channel_keys = ('X', 'Y', 'Z')

            # check if we have the required keys
            if not set(required_channel_keys).issubset(channels_keys_dict.values()):
                raise ValidationFailure(f"Correct channel keys (got {channels_keys_dict}, expected {required_channel_keys}) not found!")
            if len(channels_keys_dict.values()) != len(set(channels_keys_dict.values())):
                raise ValidationFailure(f"Channel keys ({channels_keys_dict}) contain non-unique values!")

            # Flip the channel keys in order to correctly index channels later
            flipped_channel_keys = {value : key for (key, value) in channels_keys_dict.items()}

            # we have the keys, we have the data, now process it

            # find the earliest relevant baseline
            this_pillar_id = config_df_masked_by_config_id['pillar_id'].iloc[0]
            baseline_this_pillar_subframe = baseline_df_masked_by_config_id.sort_values(by=['timestamp'])

            # grab the oldest baseline
            first_baseline = baseline_this_pillar_subframe.iloc[0]

            # baseline_timestamp_list = baseline_this_pillar_subframe.index.tolist()
            baseline_timestamp_list = baseline_this_pillar_subframe.index.get_level_values('timestamp').tolist()

            if self.request.orientation() == "HDZ":

                def apply_baseline_workhorse(dataframe_mask, time_start):
                    # after looking online (for about 5 seconds) it is "always cheaper to append to a list and create a DataFrame in one go"
                    # so let's make a 2d list of final results!
                    if dataframe_mask.empty:
                        return None
                    timestamps_return = dataframe_mask.index.to_numpy(dtype=datetime.datetime)                
                    sensor_north = dataframe_mask['data'][flipped_channel_keys['X']].to_numpy(dtype=float)
                    sensor_east = dataframe_mask['data'][flipped_channel_keys['Y']].to_numpy(dtype=float)
                    sensor_z = dataframe_mask['data'][flipped_channel_keys['Z']].to_numpy(dtype=float)
                    north_scale = float(scale_df_masked_by_config_id['correction_scale_value'][flipped_channel_keys['X']])
                    east_scale = float(scale_df_masked_by_config_id['correction_scale_value'][flipped_channel_keys['Y']])
                    zscv = float(scale_df_masked_by_config_id['correction_scale_value'][flipped_channel_keys['Z']])
                    baseline_query = baseline_df_masked_by_config_id.loc[this_pillar_id].query(f"config_id == {this_config_id} and timestamp == '{str(time_start)}'")

                    h_0 = float(baseline_query['X0'][0])
                    d_0 = float(baseline_query['Y0'][0])
                    z_0 = float(baseline_query['Z0'][0])

                    # note that pandas records foats as decimal.Decimal() objects, so we need to convert
                    h_return = np.sqrt((sensor_north * north_scale + h_0)**2 + (sensor_east * east_scale)**2)
                    d_return = d_0 * (np.pi/180.) + np.arctan2((east_scale * sensor_east), (h_0 + north_scale * sensor_north))
                    z_return = sensor_z * zscv + z_0
                    f_return = np.sqrt(np.power(h_return, 2) + np.power(z_return, 2))

                    # insertion_keys = dataframe_mask.loc[pd.IndexSlice[:, timestamps_return], :].index
                    dataframe_mask.loc[timestamps_return, [('processed_data', 'h')]] = h_return
                    dataframe_mask.loc[timestamps_return, [('processed_data', 'd')]] = d_return
                    dataframe_mask.loc[timestamps_return, [('processed_data', 'z')]] = z_return
                    dataframe_mask.loc[timestamps_return, [('processed_data', 'f')]] = f_return

                    return dataframe_mask

                if len(baseline_timestamp_list) > 0:
                    # if we have more than one entry, we need to handle the inbetweens first
                    for time_end, time_start in zip(baseline_timestamp_list[1:], baseline_timestamp_list[:-1]):
                        # use this baseline timestamp for now until the next one. Skip the last one.
                        this_mask = np.logical_and((data_df_masked_by_config_id.index >= time_start), (data_df_masked_by_config_id.index < time_end))
                        return_mask = apply_baseline_workhorse(data_df_masked_by_config_id.loc[this_mask], time_start) 
                        if return_mask is not None:
                            data_df_masked_by_config_id.loc[this_mask] = return_mask  

                    # run the last timestamp
                    time_start = baseline_timestamp_list[-1] # use this baseline timestamp for now until the next one. Skip the last one.
                    this_mask = data_df_masked_by_config_id.index >= time_start
                    return_mask = apply_baseline_workhorse(data_df_masked_by_config_id.loc[this_mask], time_start) 
                    if return_mask is not None:
                        data_df_masked_by_config_id.loc[this_mask] = return_mask  

        return info['data']
        
    def filter(self, info):
        # some tables need to be pivtoed or reindexed
        # handle data table
        # pivot the data table to properly have one timestamp and multiple channel data
        info['data'] = info['data'].pivot(index=['config_id', 'timestamp'], columns=['channel_number'], values=['data', 'flag'])

        # handle baseline table
        info['baseline'].set_index(['pillar_id', 'timestamp'], inplace=True)

        # handle meta table
        info['meta'].set_index(['config_id'], inplace=True)

        # handle scale table
        # pivot the scale table to single columns
        info['scale'] = info['scale'].pivot(index=['config_id'], columns=['channel_number'], values=['channel_key', 'voltage_scale_value', 'correction_scale_value', 'offset_value'])

        return info
        
    def build_metas(self, info):
        return [TableMetaData()]
        
    def processing_step(self):
        #TODO make the actual filtering step
        result = {}
        locations = {location for location in self.data['locations']['iaga_code']}
        for location in locations:
            info = self.split_location(location)
            info = self.filter(info)
            self.validate(info)
            if self.request.baselines() == 'yes':
                info['data'] = self.apply_baseline(info)
            metas = self.build_metas(info)
            result[location] = (info['data'], info['meta'])
        return result
        
    def request_data(self):
        time_start = self.request.start_date()
        time_end = self.request.end_date()
        # time_end = datetime.datetime.combine(time_end, datetime.time.max)
        
        stations = self.request.locations()
        if len(stations) < 1: raise EmptyResult("No valid locations selected")
        stations_as_sql = ', '.join(f"'{station}'" for station in stations)
        quality = self.request.quality()
        
        with self.get_connection() as connection:
            sql_locations = f"""SELECT `config_id` as `id`, 
            `iaga_code` as `iaga_code`, 
            `pillar_id` as `pillar_id`
            FROM `variometer_config_overview` 
            WHERE `iaga_code` IN ({stations_as_sql})"""
                        
            sql_string = f"""SELECT `timestamp`,
            `config_id`,
            `channel_number`,
            `data`,
            `flag`,
            config.`iaga_code` as `iaga_code`
            FROM variometer_data_filtered 
            INNER JOIN ({sql_locations}) config 
            ON variometer_data_filtered.`config_id` = config.`id` 
            WHERE `timestamp` BETWEEN '{time_start}' AND '{time_end}'"""

            sql_baseload = f"""SELECT baseline_data.`pillar_id` as `pillar_id`, 
            `timestamp`, 
            `Xa`, 
            `Ya`, 
            `Za`, 
            `X0`, 
            `Y0`, 
            `Z0`, 
            `D0`, 
            `I0`, 
            `N1`, 
            `N2`, 
            `N3`, 
            `N4`, 
            `offset_dD`, 
            `offset_dI`, 
            `offset_dF`, 
            `status`, 
            `type`, 
            `id` AS `config_id`, 
            `iaga_code` 
            FROM baseline_data 
            INNER JOIN ({sql_locations}) config ON baseline_data.`pillar_id` = config.`pillar_id`"""

            sql_metaload = """ SELECT variometer_config.id AS `config_id`,
            variometer_config.revision_timestamp,
            variometer_config.install_timestamp,
            variometer_config.pillar_id,
            variometer_config.sensor_id,
            variometer_config.electronics_id,
            variometer_config.adc_id,
            variometer_config.datalogger_id,
            variometer_config.revision_id,
            pillar_info.location_id,
            pillar_info.reference_number,
            pillar_info.description AS `pillar_info_desc`,
            pillar_info.geo_lat,
            pillar_info.geo_long,
            pillar_info.geo_alt,
            pillar_info.pillar_reference,
            pillar_info.comment AS `pillar_info_comment`,
            adc_info.serial_number AS `adc_serial_number`,
            adc_info.manufacturer,
            adc_info.model,
            adc_info.description AS `adc_info_desc`,
            adc_info.comment AS `adc_info_comment`,
            datalogger_info.serial_number AS `datalogger_serial_number`,
            datalogger_info.operating_system,
            datalogger_info.hardware_info,
            datalogger_info.description AS `datalogger_info_desc`,
            datalogger_info.comment AS `datalogger_info_comment`,
            electronics_info.serial_number AS `electronics_serial_number`,
            electronics_info.model AS `electronics_model`,
            electronics_info.calibration_delta_1,
            electronics_info.calibration_delta_2,
            electronics_info.calibration_delta_3,
            electronics_info.description AS `electronics_info_desc`,
            electronics_info.comment AS `electronics_info_comment`,
            location_info.display_name_long,
            location_info.display_name_short,
            location_info.display_name_IAGA_code AS `iaga_code`,
            location_info.contact,
            revision_info.comment AS `revision_info_comment`,
            revision_info.group_delay,
            revision_info.filter_description,
            revision_info.datalogger_software_version,
            revision_info.number_of_channels,
            revision_info.data_filtered_rate_hz,
            revision_info.data_sampling_rate_hz,
            revision_info.sensor_orientation,
            sensor_info.serial_number AS `sensor_serial_number`,
            sensor_info.model AS `sensor_model`,
            sensor_info.sensor_group,
            sensor_info.description AS `sensor_info_desc`,
            sensor_info.comment AS `sensor_info_comment`
            FROM variometer_config
            LEFT JOIN pillar_info
            ON variometer_config.pillar_id = pillar_info.id
            LEFT JOIN location_info
            ON pillar_info.location_id = location_info.id
            LEFT JOIN sensor_info
            ON variometer_config.sensor_id = sensor_info.id
            LEFT JOIN electronics_info
            ON variometer_config.electronics_id = electronics_info.id
            LEFT JOIN adc_info
            ON variometer_config.adc_id = adc_info.id
            LEFT JOIN datalogger_info
            ON variometer_config.datalogger_id = datalogger_info.id
            LEFT JOIN revision_info
            ON variometer_config.revision_id = revision_info.id
            """ + f" WHERE location_info.display_name_IAGA_code IN ({stations_as_sql})"

            sql_scaleload = """ SELECT variometer_config.id AS `config_id`,
            location_info.display_name_IAGA_code AS `iaga_code`,
            variometer_channel_info.channel_number AS `channel_number`,
            variometer_channel_info.key AS `channel_key`,
            variometer_channel_info.voltage_scale_value AS `voltage_scale_value`,
            variometer_channel_info.correction_scale_value AS `correction_scale_value`,
            variometer_channel_info.offset_value AS `offset_value` 
            FROM variometer_config
            INNER JOIN variometer_channel_info
            ON variometer_config.id = variometer_channel_info.config_id
            LEFT JOIN pillar_info
            ON variometer_config.pillar_id = pillar_info.id
            LEFT JOIN location_info
            ON pillar_info.location_id = location_info.id
            """ + f" WHERE location_info.display_name_IAGA_code IN ({stations_as_sql})"

            locations = load_pandas(connection, sql_locations)
            data = load_pandas(connection, sql_string)
            baseline = load_pandas(connection, sql_baseload)
            meta = load_pandas(connection, sql_metaload)
            scale = load_pandas(connection, sql_scaleload)
            self.logger.info(f"loaded data with main data {len(data)} rows and {', '.join(data.columns)} as columns")
                
            return {'main':data, 'baseline':baseline, 'locations':locations, 'meta': meta, 'scale': scale}

class FileData(Data):
    def get_data(self):
        return self.read_file(self.get_file())
        
    def get_file(self):
        return self.request.filepath()
        
    def readtype(self, file):
        # TODO make it figure out when the file requires binary, or overwrite this when neccessary
        return 'r'
        
    def get_stream(self, file):
        return file if isinstance(file, io.IOBase) else open(file, self.readtype(file))
        
    def read_file(self, file):
        with self.get_stream(file) as f:
            result = f.read()
        return result
    
class DownloadableData(FileData):
    def get_url(self):
        return self.request.url()
    
    def get_query(self):
        args = self.request.args
        result = '?' + '&'.join(f"{key}={value}" for key, value in args.items())
        return result if result else ''
        
    def build_url(self, protocol=None):
        if protocol is None:
            protocol = 'http'
        return f'{protocol}://'+self.get_url()+self.get_query()
    
    def download_stream(self, url=None):
        if url is None:
            url = self.build_url()
        response = requests.get(url, stream=True)
        return response.raw
    
    def get_file(self):
        return self.download_stream(self.build_url())
        

class SmartSourceData(DownloadableData):
    def __init__(self, *args, is_local=None, download=None, **kwargs):
        if download is not None:
            is_local = not(download)
        self.is_local = is_local
        super().__init__(*args, **kwargs)

    def get_file(self):
        if self.is_local is not None:
            return (FileData if self.is_local else DownloadableData).get_file(self)
        return self.smart_file_choice()
        
    def smart_file_choice(self):
        protocol = self.request.protocol()
        if protocol is not None:
            return self.download_stream(build_url(protocol))
        else:
            filepath = self.request.filepath()
            if filepath is not None and filepath.exists() and not filepath.is_dir():
                return filepath
            else:
                return self.download_stream()
            

        
class JsonData(SmartSourceData):
    def to_common_format(self, data):
        return {
            location:(pd.DataFrame(content[0]),
                [TableMetaData(*meta['args'],**meta['kwargs']) for meta in content[1]])
            for location, content in data.items()}

    def interpret_data(self):
        return self.to_common_format(json.loads(self.data))
        
# class JsonSmartData(SmartSourceData, JsonData):
    # pass
        
# class FromServerData(DownloadableData, JsonData):
    # pass
