class Lightbulb {
  final int id;
  String status; // <- Modyfikowany lokalnie
  final int? sensorId;

  Lightbulb({required this.id, required this.status, this.sensorId});

  factory Lightbulb.fromJson(Map<String, dynamic> json) => Lightbulb(
        id: json['id'],
        status: json['status'],
        sensorId: json['sensor_id'],
      );
}
