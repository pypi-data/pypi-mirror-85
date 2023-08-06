from .base import *


import json
import zipfile
import io
import datetime


def register_format(*names):
    def decorator(cls):
        for name in names:
            FORMAT_LIBRARY[name] = cls
        return cls
    return decorator



class PandaJSON(json.JSONEncoder):
    def default(self, obj):
        return json.loads(obj.to_json()) if hasattr(obj, 'to_json') else super().default(obj)
        # pandas seem to not do things "just" the same/Timestamp needs to be handled too.
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif hasattr(obj, 'to_json'):
            return json.loads(obj.to_json())
        else:
            return super().default(obj)


@register_format('default','json')   
class ReturnFormat:
    def __init__(self, data, ending='json',is_binary=False, **options):
        # super().__init__(data, ending, is_binary, **options)
        self.data = data
        self.ending = ending
        self.is_binary = is_binary
        self.mimetype = "text/"+self.ending
        self.headers = {"Content-Disposition": "attachment;filename=data."+self.ending}
        self._content = None
        
    def build_content(self):
        return json.dumps(self.data.data_out, cls=PandaJSON)
        
    @property
    def content(self):
        if self._content is None:
            self._content = self.build_content()
        return self._content
        
    def __iter__(self):
        yield self.content
        
    def to_file(self, path):
        with open(path, 'wb' if self.is_binary else 'w') as f:
            f.write(self.content)
       
    def as_file_stream(self, at_start=True):
        stream = io.BytesIO() if self.is_binary else io.StringIO()
        stream.write(self.content)
        if at_start:
            stream.seek(0)
        return stream
       
    # def build_return(self):
        # return Response(self, mimetype=self.mimetype, headers = self.headers)


class ZipFormat(ReturnFormat):
    def __init__(self, data, ending=None):
        super().__init__(data, 'zip')
        self.mimetype = "application/zip"

    def files(self):
        return {}

    def __iter__(self):
        result = io.BytesIO()
        with zipfile.ZipFile(result, 'w') as zip:
            for filename, content in self.files().items():
                zip.writestr(filename, str.encode(content, 'utf-8'))
        yield result.getvalue()

@register_format('IAGA-2002')   
class IAGAFormat(ZipFormat):

    def files(self):
        files_dict = {}
        # cycle through locations as list
        locations = list(self.data.data_out.keys())
        for location in locations:
            # should be a 2 element tuple, first element is data dataframe, second element is meta dataframe
            files_dict = {**files_dict, **self.process_location(location)}
        return files_dict

    def process_day(self, today, data_df_masked_by_config_id):
        body_str = ""

        # placeholder IAGA-Like data
        def reformat_line(timestamp, x, y, z, f):
            """Reformats the GeomagLogger data format into IAGA-like"""

            # TODO handle NANs and convert them to 99999.00
            try:
                day_of_year = timestamp.timetuple().tm_yday
                timestamp_splits = timestamp.strftime("%Y %m %d %H %M %S.%f").split()
                x_str = str(x)             
                y_str = str(y)             
                z_str = str(z)             
                f_str = str(f)         
                return f"{timestamp_splits[0]}-{timestamp_splits[1]}-{timestamp_splits[2]} {timestamp_splits[3]}:{timestamp_splits[4]}:{timestamp_splits[5][:6]} {day_of_year:03d}   {x_str:<9.9} {y_str:<9.9} {z_str:<9.9} {f_str:<9.9}\n"
            except Exception as ex:                
                raise ex
                return ''

        # write to file
        # insert header

        for timestamp, x, y, z, f in zip(data_df_masked_by_config_id.index.to_numpy(dtype=datetime.datetime),
                                            data_df_masked_by_config_id[('processed_data', 'h')],
                                            data_df_masked_by_config_id[('processed_data', 'd')],
                                            data_df_masked_by_config_id[('processed_data', 'z')],
                                            data_df_masked_by_config_id[('processed_data', 'f')]):
            # read the line in, transform it, then write out to staging
            if (timestamp >= today) and (timestamp < (today + datetime.timedelta(days=1))):
                body_str += reformat_line(timestamp, x, y, z, f)

        return body_str

    def process_location(self, location_to_process):

        # define a standard header generator for IAGA-2002 files
        def header_generator(station_metadata_dict):
            # IAGA header file generation
            yield f"Format                  IAGA-2002                                    |\n"
            yield f"Source of Data          {station_metadata_dict['station_owner']:<45}|\n"
            yield f"Station Name            {station_metadata_dict['station_name']:<45}|\n"
            yield f"IAGA CODE               {station_metadata_dict['iaga_code']:<45}|\n"
            yield f"Geodetic Latitude       {station_metadata_dict['station_lat']:<45}|\n"
            yield f"Geodetic Longitude      {station_metadata_dict['station_long']:<45}|\n"
            yield f"Elevation               {station_metadata_dict['station_alt']:<45}|\n"
            yield f"Reported                Xs Ys Zs F                                   |\n"
            yield f"Sensor Orientation      {station_metadata_dict['sensor_orientation']:<45}|\n"
            yield f"Digital Sampling        {station_metadata_dict['data_sampling']:<45}|\n"
            yield f"Data Interval Type      {station_metadata_dict['data_interval']:<45}|\n"
            yield f"Data Type               {station_metadata_dict['data_type']:<45}|\n"
            yield f"DATE       TIME         DOY   Xs [nT]   Ys [nT]   Zs [nT]   F [nT]   |\n"

        # we should have all baselines applies, and each IAGA code location in a table
        # need to check to make sure we have unique timestamps

        # open a file object to pass back
        return_dict = {}

        # cycle through config ids
        for this_config_id, config_df_masked_by_config_id in self.data.data_out[location_to_process][1].groupby(level=0):

            # create a metadata dictionary to hand over to the IAGA file generator
            # TODO insert fields for data_interval, data_type
            station_metadata_dict = {'station_owner': 'DTU',
                'station_name': config_df_masked_by_config_id['display_name_long'].iloc[0],
                'iaga_code': config_df_masked_by_config_id['iaga_code'].iloc[0],
                'station_lat': f"{config_df_masked_by_config_id['geo_lat'].iloc[0]:<5.5}",
                'station_long': f"{config_df_masked_by_config_id['geo_long'].iloc[0]:<5.5}",
                'station_alt': f"{config_df_masked_by_config_id['geo_alt'].iloc[0]:<5.5}",
                'sensor_orientation': config_df_masked_by_config_id['sensor_orientation'].iloc[0],
                'data_sampling': f"{config_df_masked_by_config_id['data_sampling_rate_hz'].iloc[0]:<5.5} Hz",
                'data_interval': f"{config_df_masked_by_config_id['data_filtered_rate_hz'].iloc[0]:<5.5} Hz",
                'data_type': 'Variometer'
            }


            if this_config_id not in self.data.data_out[location_to_process][0].index.get_level_values('config_id'):
                # We didn't find the config ID in the data out
                continue
            data_df_masked_by_config_id = self.data.data_out[location_to_process][0].loc[this_config_id, :] 

            # cycle through days
            start_date = min(data_df_masked_by_config_id.index)
            end_date = max(data_df_masked_by_config_id.index)
            timestamp_delta = end_date - start_date
            for delta_day in range(timestamp_delta.days + 1):
                datetime_today = start_date + datetime.timedelta(delta_day)
                filename_str = f"{location_to_process}{datetime_today.strftime('%Y%m%d')}.sec"

                # start the return string
                return_str = ""
                # insert the header
                for this_line in header_generator(station_metadata_dict):
                    return_str += this_line
                # insert the body
                return_str += self.process_day(datetime_today, data_df_masked_by_config_id)

                return_dict[filename_str] = return_str


        return return_dict
