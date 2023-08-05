from localstack.utils.aws import aws_models
IMukb=super
IMukf=None
IMukN=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  IMukb(LambdaLayer,self).__init__(arn)
  self.cwd=IMukf
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.IMukN.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,IMukN,env=IMukf):
  IMukb(RDSDatabase,self).__init__(IMukN,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,IMukN,env=IMukf):
  IMukb(RDSCluster,self).__init__(IMukN,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,IMukN,env=IMukf):
  IMukb(AppSyncAPI,self).__init__(IMukN,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,IMukN,env=IMukf):
  IMukb(AmplifyApp,self).__init__(IMukN,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,IMukN,env=IMukf):
  IMukb(ElastiCacheCluster,self).__init__(IMukN,env=env)
class TransferServer(BaseComponent):
 def __init__(self,IMukN,env=IMukf):
  IMukb(TransferServer,self).__init__(IMukN,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,IMukN,env=IMukf):
  IMukb(CloudFrontDistribution,self).__init__(IMukN,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,IMukN,env=IMukf):
  IMukb(CodeCommitRepository,self).__init__(IMukN,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
