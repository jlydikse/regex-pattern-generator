# from app import db

# class OCRResult(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.Text, nullable=False)
#     regex_patterns = db.relationship('RegexPattern', backref='ocr_result', lazy=True)

# class RegexPattern(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     pattern = db.Column(db.String(200), nullable=False)
#     ocr_result_id = db.Column(db.Integer, db.ForeignKey('OCRResult.id'), nullable=False)
